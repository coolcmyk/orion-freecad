# Local FreeCAD MCP setup

Prepared on 2026-10-10 using [neka-nat/freecad-mcp](https://github.com/neka-nat/freecad-mcp), version 0.1.26, with its MIT license retained. The downloaded `main` archive SHA-256 was `ac0fe466e2af99fb8cf19cae910c248af7c2d2bf4dbe91171198fc71cfc1a7e1`. Dependencies are pinned by the upstream `uv.lock`.

Run from a local terminal:

```bash
bash /home/kyo/ws/orion/tools/setup_freecad_mcp.sh
```

This installs the external MCP server in `tools/freecad-mcp/.venv` and registers its STDIO command with Codex. It needs internet access for Python dependencies and write access to your Codex configuration. The server requires Python >=3.12; this machine has `/usr/bin/python` 3.14.7.

In the existing FreeCAD window, enable **View → Panels → Python console** and run:

```python
exec(open('/home/kyo/ws/orion/tools/start_freecad_mcp.FCMacro').read())
```

Alternatively open and execute that file using FreeCAD's Macro dialog. The macro loads the addon from this workspace and starts its bridge on `127.0.0.1:9875`. It does not require copying files into the FreeCAD addon directory and does not modify any CAD documents. Run the macro again after restarting FreeCAD.

Restart the FreeCAD MCP connection in Codex's MCP settings to load its tools. [Official MCP setup documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

To verify from a local terminal:

```bash
python -c "import socket, xmlrpc.client; socket.setdefaulttimeout(5); bridge = xmlrpc.client.ServerProxy('http://127.0.0.1:9875'); print(bridge.ping()); print(bridge.get_rpc_status())"
```

Expect `True` and an RPC status report. Port 9875 is an XML-RPC bridge, not an HTTP MCP endpoint; use the registered STDIO command for Codex.

## Current status

Activated by the user and verified through MCP on 2026-10-10: server and addon 0.1.26, protocol version 1, healthy GUI dispatch. FreeCAD 1.1.3 is connected and the ORION fit-prototype model has been built. The earlier sandbox restrictions required running setup and the macro from the host terminal/FreeCAD console.

To stop the bridge in FreeCAD:

```python
from rpc_server import rpc_server as orion_bridge
orion_bridge.stop_rpc_server()
```

To remove the Codex registration, run `codex mcp remove freecad` in a local terminal.
