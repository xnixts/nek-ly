#!/usr/bin/env python3
"""Nek Ly: a small, customizable command interface for Termux."""
import json
import os
import platform
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

APP_NAME = "Nek Ly"
VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"


def load_config():
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"name": APP_NAME, "version": VERSION, "tagline": "Your Linux learning environment"}


def banner():
    config = load_config()
    print(r"""
 _   _ _____ _  __   _  __
| \ | | ____| |/ /  | |/ /
|  \| |  _| | ' /   | ' /
| |\  | |___| . \   | . \
|_| \_|_____|_|\_\  |_|\_\
""")
    print(f"       {config.get('name', APP_NAME)} {VERSION}")
    print(f"       {config.get('tagline', '')}\n")


def help_text():
    print("""Nek Ly commands:
  help             Show this help
  info             Show Nek Ly and device information
  files [path]     List files in a directory
  where            Show current working directory
  py               Open the Python interactive shell
  linux            Open the Debian environment (if installed)
  install-linux    Install Debian using proot-distro
  update           Update Termux packages
  clear            Clear the screen
  exit             Exit Nek Ly

Nek Ly runs in Termux. Linux features use proot-distro and do not
grant Android root access. Only use security tools on systems you own
or have explicit permission to test.
""")


def show_info():
    print(f"Name:         {APP_NAME}")
    print(f"Version:      {VERSION}")
    print(f"Python:       {platform.python_version()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Platform:     {platform.platform()}")
    print(f"Termux home:  {Path.home()}")
    print(f"Linux base:   {'Debian (proot-distro)' if shutil.which('proot-distro') else 'not installed'}")


def list_files(path="."):
    target = Path(path).expanduser()
    try:
        for item in sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower())):
            suffix = "/" if item.is_dir() else ""
            print(f"{item.name}{suffix}")
    except OSError as exc:
        print(f"Cannot list {target}: {exc}")


def install_linux():
    if not shutil.which("proot-distro"):
        print("proot-distro is missing. In Termux run: pkg install proot-distro")
        return
    result = subprocess.run(["proot-distro", "list"], check=False, text=True, capture_output=True)
    if "debian" in result.stdout.lower() and "installed" in result.stdout.lower():
        print("Debian appears to already be installed. Try: nekly linux")
        return
    print("Installing Debian. This downloads packages and may take some time...")
    subprocess.run(["proot-distro", "install", "debian"], check=False)


def open_linux():
    if not shutil.which("proot-distro"):
        print("Install proot-distro first: pkg install proot-distro")
        return
    result = subprocess.run(["proot-distro", "list"], check=False, text=True, capture_output=True)
    if "debian" not in result.stdout.lower() or "installed" not in result.stdout.lower():
        print("Debian is not installed yet. Run: nekly install-linux")
        return
    subprocess.run(["proot-distro", "login", "debian"], check=False)


def run_command(line):
    try:
        args = shlex.split(line)
    except ValueError as exc:
        print(f"Input error: {exc}")
        return True
    if not args:
        return True

    cmd = args[0].lower()
    if cmd in {"exit", "quit"}:
        return False
    if cmd in {"help", "--help", "-h"}:
        help_text()
    elif cmd == "info":
        show_info()
    elif cmd == "files":
        list_files(args[1] if len(args) > 1 else ".")
    elif cmd == "where":
        print(Path.cwd())
    elif cmd == "py":
        subprocess.run([sys.executable, "-i"], check=False)
    elif cmd == "linux":
        open_linux()
    elif cmd == "install-linux":
        install_linux()
    elif cmd == "update":
        if shutil.which("pkg"):
            subprocess.run(["pkg", "update"], check=False)
            subprocess.run(["pkg", "upgrade", "-y"], check=False)
        else:
            print("The pkg command is available only in Termux.")
    elif cmd == "clear":
        os.system("clear")
    else:
        print(f"Unknown command: {cmd}. Type 'help'.")
    return True


def main():
    banner()
    print("Type 'help' to see available commands.\n")
    while True:
        try:
            if not run_command(input("nekly > ")):
                print("Nek Ly closed.")
                break
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit.")
        except EOFError:
            print()
            break


if __name__ == "__main__":
    main()
