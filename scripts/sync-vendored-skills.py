#!/usr/bin/env python3
"""Sync vendored third-party skills from pinned upstream snapshots."""

from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = REPO_ROOT / "vendored-skills.json"
NOTICES_PATH = REPO_ROOT / "THIRD_PARTY_NOTICES.md"
USER_AGENT = "Addono-skills-vendor-sync/1.0"


def safe_join(base: Path, relative_path: str) -> Path:
    candidate = (base / relative_path).resolve()
    base_resolved = base.resolve()
    if candidate != base_resolved and base_resolved not in candidate.parents:
        raise ValueError(f"Path escapes base directory: {relative_path}")
    return candidate


def fetch_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request) as response:
        return response.read()


def fetch_json(url: str) -> dict[str, Any]:
    return json.loads(fetch_bytes(url).decode("utf-8"))


def safe_extract(tar: tarfile.TarFile, destination: Path) -> None:
    destination_resolved = destination.resolve()
    for member in tar.getmembers():
        member_path = (destination / member.name).resolve()
        if member_path != destination_resolved and destination_resolved not in member_path.parents:
            raise ValueError(f"Archive member escapes destination: {member.name}")
    tar.extractall(destination)


def load_manifest() -> dict[str, Any]:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def dump_manifest(manifest: dict[str, Any]) -> str:
    return json.dumps(manifest, indent=2) + "\n"


def write_text(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else None
    if existing == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def write_bytes(path: Path, content: bytes) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_bytes() if path.exists() else None
    if existing == content:
        return False
    path.write_bytes(content)
    return True


def render_vendored_metadata(skill: dict[str, Any]) -> str:
    payload = {
        "name": skill["name"],
        "destination": skill["destination"],
        "generated_by": "scripts/sync-vendored-skills.py",
        "upstream": {
            "type": skill["upstream"]["type"],
            "repository": skill["upstream"]["repository"],
            "path": skill["upstream"]["path"],
            "ref": skill["upstream"]["ref"],
            "track_branch": skill["upstream"]["track_branch"],
        },
        "license": skill["license"],
        "files": skill["files"],
        "allow_local_modifications": skill["allow_local_modifications"],
    }
    return json.dumps(payload, indent=2) + "\n"


def render_attribution(skill: dict[str, Any], has_notice: bool) -> str:
    upstream = skill["upstream"]
    source_url = f"https://github.com/{upstream['repository']}/tree/{upstream['ref']}/{upstream['path']}"
    notice_line = "[NOTICE.upstream](NOTICE.upstream)" if has_notice else "Not present upstream"
    imported_files = "\n".join(f"- `{path}`" for path in skill["files"])
    status = (
        "This vendored snapshot must stay byte-for-byte aligned with upstream."
        if not skill["allow_local_modifications"]
        else "Local modifications are permitted and must be documented when they occur."
    )
    return f"""# Vendored Attribution

This directory is generated from a pinned upstream snapshot by `scripts/sync-vendored-skills.py`.

## Upstream

- Repository: `{upstream["repository"]}`
- Path: `{upstream["path"]}`
- Pinned commit: `{upstream["ref"]}`
- Tracking branch: `{upstream["track_branch"]}`
- Source snapshot: {source_url}

## License

- SPDX identifier: `{skill["license"]["spdx_id"]}`
- Copyright owner: `{skill["license"]["copyright_owner"]}`
- Upstream license file: [LICENSE.upstream](LICENSE.upstream)
- Upstream notice file: {notice_line}

## Imported files

{imported_files}

## Local modifications

- Allowed: `{str(skill["allow_local_modifications"]).lower()}`
- Status: {status}
"""


def render_third_party_notices(skills: list[dict[str, Any]]) -> str:
    sections: list[str] = [
        "# Third-Party Notices",
        "",
        "This repository includes vendored third-party skills generated from pinned upstream snapshots via `scripts/sync-vendored-skills.py`.",
        "",
    ]
    for skill in skills:
        upstream = skill["upstream"]
        sections.extend(
            [
                f"## {skill['name']}",
                "",
                f"- Installed path: `{skill['destination']}`",
                f"- Upstream repository: `{upstream['repository']}`",
                f"- Upstream path: `{upstream['path']}`",
                f"- Pinned commit: `{upstream['ref']}`",
                f"- Tracking branch: `{upstream['track_branch']}`",
                f"- License: `{skill['license']['spdx_id']}`",
                f"- Copyright owner: `{skill['license']['copyright_owner']}`",
                f"- Local modifications allowed: `{str(skill['allow_local_modifications']).lower()}`",
                f"- Attribution: `{skill['destination']}/ATTRIBUTION.md`",
                "",
            ]
        )
    return "\n".join(sections).rstrip() + "\n"


def latest_commit_sha(repository: str, branch: str) -> str:
    url = f"https://api.github.com/repos/{repository}/commits/{branch}"
    payload = fetch_json(url)
    sha = payload.get("sha")
    if not sha:
        raise ValueError(f"Unable to determine latest commit for {repository}@{branch}")
    return sha


def load_archive(repository: str, ref: str, cache: dict[tuple[str, str], Path], temp_root: Path) -> Path:
    cache_key = (repository, ref)
    if cache_key in cache:
        return cache[cache_key]

    archive_url = f"https://codeload.github.com/{repository}/tar.gz/{ref}"
    archive_bytes = fetch_bytes(archive_url)
    extract_root = temp_root / f"{repository.replace('/', '--')}-{ref}"
    extract_root.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as tar:
        safe_extract(tar, extract_root)
    roots = [path for path in extract_root.iterdir() if path.is_dir()]
    if len(roots) != 1:
        raise ValueError(f"Expected one root directory in archive for {repository}@{ref}")
    cache[cache_key] = roots[0]
    return roots[0]


def expected_outputs(skill: dict[str, Any], archive_root: Path) -> dict[Path, bytes]:
    upstream = skill["upstream"]
    upstream_root = safe_join(archive_root, upstream["path"])
    outputs: dict[Path, bytes] = {}
    destination_root = safe_join(REPO_ROOT, skill["destination"])

    for relative_path in skill["files"]:
        source_path = safe_join(upstream_root, relative_path)
        outputs[safe_join(destination_root, relative_path)] = source_path.read_bytes()

    license_path = safe_join(archive_root, upstream["license_file"])
    outputs[destination_root / "LICENSE.upstream"] = license_path.read_bytes()

    notice_path = safe_join(archive_root, upstream["notice_file"])
    if notice_path.exists():
        outputs[destination_root / "NOTICE.upstream"] = notice_path.read_bytes()

    outputs[destination_root / "VENDORED.json"] = render_vendored_metadata(skill).encode("utf-8")
    outputs[destination_root / "ATTRIBUTION.md"] = render_attribution(skill, notice_path.exists()).encode("utf-8")
    return outputs


def sync_skill(skill: dict[str, Any], archive_root: Path, check: bool) -> list[str]:
    outputs = expected_outputs(skill, archive_root)
    destination_root = safe_join(REPO_ROOT, skill["destination"])
    changes: list[str] = []

    for path, expected_content in outputs.items():
        if check:
            if not path.exists():
                changes.append(f"missing {path.relative_to(REPO_ROOT)}")
                continue
            current_content = path.read_bytes()
            if current_content != expected_content:
                changes.append(f"stale {path.relative_to(REPO_ROOT)}")
            continue

        if isinstance(expected_content, bytes):
            changed = write_bytes(path, expected_content)
            if changed:
                changes.append(f"updated {path.relative_to(REPO_ROOT)}")

    notice_file = destination_root / "NOTICE.upstream"
    if notice_file not in outputs and notice_file.exists():
        if check:
            changes.append(f"unexpected {notice_file.relative_to(REPO_ROOT)}")
        else:
            notice_file.unlink()
            changes.append(f"removed {notice_file.relative_to(REPO_ROOT)}")

    return changes


def sync_all(skills: list[dict[str, Any]], check: bool) -> list[str]:
    changes: list[str] = []
    archive_cache: dict[tuple[str, str], Path] = {}
    with tempfile.TemporaryDirectory(prefix="vendored-skills-") as temp_dir:
        temp_root = Path(temp_dir)
        for skill in skills:
            archive_root = load_archive(skill["upstream"]["repository"], skill["upstream"]["ref"], archive_cache, temp_root)
            changes.extend(sync_skill(skill, archive_root, check))

    notices_content = render_third_party_notices(skills).encode("utf-8")
    if check:
        if not NOTICES_PATH.exists():
            changes.append(f"missing {NOTICES_PATH.relative_to(REPO_ROOT)}")
        elif NOTICES_PATH.read_bytes() != notices_content:
            changes.append(f"stale {NOTICES_PATH.relative_to(REPO_ROOT)}")
    elif write_bytes(NOTICES_PATH, notices_content):
        changes.append(f"updated {NOTICES_PATH.relative_to(REPO_ROOT)}")

    return changes


def update_pinned_refs(manifest: dict[str, Any]) -> bool:
    updated = False
    for skill in manifest["skills"]:
        upstream = skill["upstream"]
        latest_ref = latest_commit_sha(upstream["repository"], upstream["track_branch"])
        if latest_ref != upstream["ref"]:
            upstream["ref"] = latest_ref
            updated = True
    if updated:
        write_text(MANIFEST_PATH, dump_manifest(manifest))
    return updated


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify generated vendored files are up to date")
    parser.add_argument(
        "--update-pinned-refs",
        action="store_true",
        help="update manifest refs to the latest commit on each tracked branch before syncing",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = load_manifest()

    try:
        if args.update_pinned_refs:
            updated = update_pinned_refs(manifest)
            if updated:
                manifest = load_manifest()
                print(f"Updated pinned refs in {MANIFEST_PATH.relative_to(REPO_ROOT)}")

        changes = sync_all(manifest["skills"], check=args.check)
    except (OSError, ValueError, urllib.error.URLError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.check:
        if changes:
            print("Vendored skills are out of date:")
            for change in changes:
                print(f"- {change}")
            return 1
        print("Vendored skills are up to date.")
        return 0

    if changes:
        for change in changes:
            print(change)
    else:
        print("No vendored skill changes detected.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
