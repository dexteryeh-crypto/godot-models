#!/usr/bin/env python3
import argparse
import json
import os
import select
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


DEFAULT_COMMAND = str(Path.home() / ".codex" / "mcp" / "godot-mcp.sh")


def encode_message(message: dict[str, Any]) -> bytes:
    body = json.dumps(message, separators=(",", ":")).encode("utf-8")
    return b"Content-Length: " + str(len(body)).encode("ascii") + b"\r\n\r\n" + body


def read_exact(stream, byte_count: int, deadline: float) -> bytes:
    chunks: list[bytes] = []
    remaining = byte_count
    fd = stream.fileno()

    while remaining > 0:
        timeout = deadline - time.monotonic()
        if timeout <= 0:
            raise TimeoutError(f"timed out while reading {remaining} response bytes")

        readable, _, _ = select.select([fd], [], [], timeout)
        if not readable:
            raise TimeoutError(f"timed out while reading {remaining} response bytes")

        chunk = os.read(fd, remaining)
        if not chunk:
            raise EOFError("server closed stdout")
        chunks.append(chunk)
        remaining -= len(chunk)

    return b"".join(chunks)


def read_message(stream, timeout_seconds: float) -> dict[str, Any]:
    deadline = time.monotonic() + timeout_seconds
    header = bytearray()

    while b"\r\n\r\n" not in header and b"\n\n" not in header:
        header.extend(read_exact(stream, 1, deadline))

    separator = b"\r\n\r\n" if b"\r\n\r\n" in header else b"\n\n"
    header_text, body_prefix = bytes(header).split(separator, 1)
    content_length = None

    for line in header_text.decode("utf-8", "replace").replace("\r", "").split("\n"):
        if line.lower().startswith("content-length:"):
            content_length = int(line.split(":", 1)[1].strip())
            break

    if content_length is None:
        raise ValueError(f"response header has no Content-Length: {header_text!r}")

    body = body_prefix
    if len(body) < content_length:
        body += read_exact(stream, content_length - len(body), deadline)

    return json.loads(body[:content_length].decode("utf-8"))


def send_request(proc: subprocess.Popen[bytes], request: dict[str, Any], timeout_seconds: float) -> dict[str, Any]:
    assert proc.stdin is not None
    assert proc.stdout is not None

    proc.stdin.write(encode_message(request))
    proc.stdin.flush()
    return read_message(proc.stdout, timeout_seconds)


def drain_stderr(proc: subprocess.Popen[bytes]) -> str:
    assert proc.stderr is not None
    fd = proc.stderr.fileno()
    output = bytearray()

    while True:
        readable, _, _ = select.select([fd], [], [], 0)
        if not readable:
            break
        chunk = os.read(fd, 65536)
        if not chunk:
            break
        output.extend(chunk)

    return output.decode("utf-8", "replace")


def print_step(label: str, started_at: float, response: dict[str, Any]) -> None:
    elapsed = time.monotonic() - started_at
    print(f"[ok] {label} responded in {elapsed:.3f}s")
    print(json.dumps(response, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe the Godot MCP stdio bridge.")
    parser.add_argument(
        "--command",
        default=DEFAULT_COMMAND,
        help=f"MCP server command to start. Default: {DEFAULT_COMMAND}",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Seconds to wait for each MCP response.",
    )
    parser.add_argument(
        "--call-tool",
        default="godot_performance.get_fps",
        help="Tool to call after tools/list. Use an empty string to skip.",
    )
    parser.add_argument(
        "--godot-host",
        default=os.environ.get("GODOT_MCP_HOST", "127.0.0.1"),
        help="Forwarded Godot TCP host.",
    )
    parser.add_argument(
        "--godot-port",
        default=os.environ.get("GODOT_MCP_PORT", "9080"),
        help="Forwarded Godot TCP port.",
    )
    args = parser.parse_args()

    env = os.environ.copy()
    env["GODOT_MCP_HOST"] = args.godot_host
    env["GODOT_MCP_PORT"] = str(args.godot_port)

    print(f"[info] starting MCP command: {args.command}")
    print(f"[info] Godot TCP backend: {env['GODOT_MCP_HOST']}:{env['GODOT_MCP_PORT']}")

    proc = subprocess.Popen(
        [args.command],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        start_new_session=True,
    )

    try:
        started = time.monotonic()
        response = send_request(
            proc,
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-03-26",
                    "capabilities": {},
                    "clientInfo": {"name": "godot-mcp-probe", "version": "1.0.0"},
                },
            },
            args.timeout,
        )
        print_step("initialize", started, response)

        assert proc.stdin is not None
        proc.stdin.write(
            encode_message({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
        )
        proc.stdin.flush()
        print("[ok] sent notifications/initialized")

        started = time.monotonic()
        response = send_request(proc, {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}, args.timeout)
        print_step("tools/list", started, response)

        if args.call_tool:
            started = time.monotonic()
            response = send_request(
                proc,
                {
                    "jsonrpc": "2.0",
                    "id": 3,
                    "method": "tools/call",
                    "params": {"name": args.call_tool, "arguments": {}},
                },
                args.timeout,
            )
            print_step(f"tools/call {args.call_tool}", started, response)

        stderr = drain_stderr(proc)
        if stderr:
            print("[stderr]")
            print(stderr.rstrip())

        return 0
    except Exception as exc:
        print(f"[fail] {exc}", file=sys.stderr)
        stderr = drain_stderr(proc)
        if stderr:
            print("[stderr]", file=sys.stderr)
            print(stderr.rstrip(), file=sys.stderr)
        return 1
    finally:
        if proc.poll() is None:
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait(timeout=2)


if __name__ == "__main__":
    raise SystemExit(main())
