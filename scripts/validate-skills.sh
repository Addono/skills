#!/usr/bin/env bash
# Validate that all skills in the skills/ directory have the required structure.
# Exit 0 on success, 1 on any failure.

set -euo pipefail

SKILLS_DIR="$(cd "$(dirname "$0")/.." && pwd)/skills"
ERRORS=0

if [ ! -d "$SKILLS_DIR" ]; then
  echo "ERROR: skills/ directory not found at $SKILLS_DIR"
  exit 1
fi

for skill_dir in "$SKILLS_DIR"/*/; do
  skill_name="$(basename "$skill_dir")"
  skill_md="$skill_dir/SKILL.md"

  # 1. SKILL.md must exist
  if [ ! -f "$skill_md" ]; then
    echo "ERROR [$skill_name]: SKILL.md not found"
    ERRORS=$((ERRORS + 1))
    continue
  fi

  # 2. Frontmatter must be present (file must start with ---)
  first_line="$(head -1 "$skill_md")"
  if [ "$first_line" != "---" ]; then
    echo "ERROR [$skill_name]: SKILL.md does not start with YAML frontmatter (---)"
    ERRORS=$((ERRORS + 1))
    continue
  fi

  # 3. Frontmatter must contain 'name:'
  if ! grep -q "^name:" "$skill_md"; then
    echo "ERROR [$skill_name]: SKILL.md frontmatter missing 'name:' field"
    ERRORS=$((ERRORS + 1))
  fi

  # 4. Frontmatter must contain 'description:'
  if ! grep -q "^description:" "$skill_md"; then
    echo "ERROR [$skill_name]: SKILL.md frontmatter missing 'description:' field"
    ERRORS=$((ERRORS + 1))
  fi

  # 5. SKILL.md should be under 200 lines (external skills are exempt if they declare 'external:')
  line_count="$(wc -l < "$skill_md")"
  is_external=false
  if grep -q "^external:" "$skill_md"; then
    is_external=true
  fi

  if [ "$is_external" = "false" ] && [ "$line_count" -gt 200 ]; then
    echo "WARN  [$skill_name]: SKILL.md is $line_count lines (recommended max: 200). Move long content to references/"
    # Warning only, not an error
  fi

  echo "OK    [$skill_name]: SKILL.md valid ($line_count lines)"
done

if [ "$ERRORS" -gt 0 ]; then
  echo ""
  echo "Validation failed with $ERRORS error(s)."
  exit 1
fi

echo ""
echo "All skills validated successfully."
