# Nek Ly

**Nek Ly** is a small, customizable Linux-learning environment for Android using Termux. It provides its own command interface and an optional Debian environment through `proot-distro`.

> This is a Termux project, not an independent operating system or a replacement for Android. It does not provide real root access.

## Features

- Custom `nekly` command
- Interactive Nek Ly shell
- `help`, `info`, `files`, `where`, `py`, `update`
- Optional Debian installation and launch
- Configuration in `config.json`

## Requirements

- Android
- Termux
- Internet connection
- Free storage for Debian if you install it

## Install from a downloaded ZIP

Extract the ZIP inside Termux-accessible storage or clone the repository, then run:

```bash
bash install.sh
```

After installation:

```bash
nekly
nekly help
nekly info
```

Optional Debian environment:

```bash
nekly install-linux
nekly linux
```

The Debian install downloads packages and can take some time. The installer does not automatically install Debian; you choose when to do that.

## Install from GitHub

Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username:

```bash
pkg update
pkg install git -y
git clone https://github.com/xnixts/nek-ly.git
cd nek-ly
bash install.sh
```

## Publish to GitHub

Create an empty public repository named `nek-ly` on GitHub. Then, in this project folder:

```bash
git init -b main
git add .
git commit -m "Nek Ly 1.0 initial release"
git remote add origin https://github.com/xnixts/nek-ly.git
git push -u origin main
```

GitHub may ask you to authenticate. Do not put passwords, access tokens, or private keys in this repository.

## Safety

Nek Ly is for learning Linux and authorized security testing. Only test devices, networks, and systems you own or have explicit permission to assess.
