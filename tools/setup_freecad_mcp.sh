#!/usr/bin/env bash
# Run in a local terminal, outside the Codex sandbox.
set -euo pipefail

tools_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
server_dir="$tools_dir/freecad-mcp"
uv_bin="$(command -v uv)"
codex_bin="$(command -v codex)"

"$uv_bin" sync --directory "$server_dir" --frozen --no-dev --python /usr/bin/python
"$server_dir/.venv/bin/freecad-mcp" --help >/dev/null
"$codex_bin" mcp add freecad -- "$server_dir/.venv/bin/freecad-mcp" --host 127.0.0.1

printf '\nFreeCAD MCP command registered. The FreeCAD bridge must also be started.\n'
printf 'In your existing FreeCAD window, open and execute this macro:\n%s\n' "$tools_dir/start_freecad_mcp.FCMacro"
printf 'Then restart the MCP connection in Codex settings.\n'

