#!/usr/bin/env bash
# LEGACY install path — copies skills + the friction-capture script into ~/.claude.
# Preferred: install as a plugin (see README). Safe to re-run.
#
# Deliberately does NOT touch ~/.claude/CLAUDE.md or ~/.claude/settings.json —
# those are your global config and may have local customisations.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${HOME}/.claude"

echo "Deploying from : $REPO"
echo "Into           : $DEST"
echo

mkdir -p "$DEST/skills" "$DEST/scripts" "$DEST/insights/friction"

# Skills (source of truth → live copy)
for d in "$REPO"/skills/*/; do
  name="$(basename "$d")"
  rm -rf "$DEST/skills/$name"
  cp -r "${d%/}" "$DEST/skills/"
  # Skills are authored for the plugin install; point the legacy copy at ~/.claude instead
  sed -i.bak 's#${CLAUDE_PLUGIN_ROOT}/#'"$DEST"'/#g' "$DEST/skills/$name/SKILL.md" && rm -f "$DEST/skills/$name/SKILL.md.bak"
  echo "  skill   : $name"
done

# Remove a stale skill that was merged into /retro
if [ -d "$DEST/skills/global-retro" ]; then
  rm -rf "$DEST/skills/global-retro"
  echo "  removed : global-retro (merged into /retro)"
fi

# Friction-capture script (run by /session-end and /retro)
cp "$REPO/scripts/retro-capture.py" "$DEST/scripts/retro-capture.py"
chmod +x "$DEST/scripts/retro-capture.py"
echo "  script  : scripts/retro-capture.py"

# Earlier versions installed the script under hooks/ — remove the orphan so
# there is exactly one copy and the skills (now pointing at scripts/) use it.
if [ -f "$DEST/hooks/retro-capture.py" ]; then
  rm -f "$DEST/hooks/retro-capture.py"
  echo "  removed : hooks/retro-capture.py (moved to scripts/)"
fi

# Capture now runs inside /session-end — warn if an old background hook lingers
if [ -f "$DEST/settings.json" ] && grep -q "retro-capture.py" "$DEST/settings.json"; then
  echo
  echo "  NOTE: ~/.claude/settings.json still wires retro-capture.py as a hook."
  echo "        Capture now runs inside /session-end — remove that SessionEnd block."
fi

cat <<'EOF'

Done.

Usage:
  • Every session, when wrapping up : /session-end      (captures friction)
  • Periodically, to consolidate    : /insights  then  /retro global
        → review the proposed changes, press Apply.
        (First /retro global will offer to create learned-rules.md and add the
         @import line to ~/.claude/CLAUDE.md — approve it.)
EOF
