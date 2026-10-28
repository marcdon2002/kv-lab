# Key-Value Databases Lab

Hands-on lab for the *Key-Value Databases* session in Database Technologies at Hochschule Aalen: run a real Redis server on your own laptop and try sessions, caching, leaderboards and atomic updates.

[![Redis](https://img.shields.io/badge/Redis_7.4.7-FF4438?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io/docs/latest/)
[![Docker](https://img.shields.io/badge/Docker_Desktop-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/products/docker-desktop/)
[![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Hochschule Aalen](https://img.shields.io/badge/Database_Technologies-Hochschule_Aalen-5A56A1?style=for-the-badge)](https://www.hs-aalen.de/)

[Download](#download) · [Setup](#setup) · [Lab start](#lab-start) · [Demos and exercises](#demos-and-exercises) · [Help](#help)

> [!TIP]
> **Sitting in the lecture right now?**
> Download your kit from the [table below](#download) and follow the setup guide for your laptop. The installation runs in the background while the theory continues. Everything is ready at **minute 48**.

## Overview

The lab runs completely on your laptop. Docker Desktop is the only program you install. Redis and the Python demo tools run inside containers.

Each kit contains the Docker images as a file. That's why the lab works **offline**, even when the whole lecture room shares one Wi-Fi connection.

You run four demos that stop at every **? Predict** question, then try three exercises yourself in `redis-cli`. The running example is a campus app with logins, unique visitors, a quiz leaderboard and a job queue.

## Download

Download **one** file, the one that matches your laptop:

| Your laptop | Kit |
| --- | --- |
| Windows (Intel/AMD) · Mac with **Intel** chip | **[kv-lab-amd64.zip](https://github.com/marcdon2002/kv-lab/releases/latest/download/kv-lab-amd64.zip)** |
| Mac with **Apple** chip (M1, M2, M3, M4 …) · Windows on ARM (Snapdragon) | **[kv-lab-arm64.zip](https://github.com/marcdon2002/kv-lab/releases/latest/download/kv-lab-arm64.zip)** |

<details>
<summary>Which chip do I have?</summary>

- **Mac:** *Apple menu → About This Mac*. *Chip: Apple …* means `arm64`, *Processor: Intel …* means `amd64`.
- **Windows:** almost always `amd64`. Only Snapdragon laptops (e.g. Surface Pro X, Copilot+ PCs with Snapdragon) need `arm64`.

A wrong kit still works on a Mac, just more slowly.

</details>

> [!WARNING]
> **Don't use the green "Code → Download ZIP" button.** That ZIP doesn't contain the Docker images
> (`images.tar.gz`). Without them, Docker tries to download the images from Docker Hub, and in the lecture Wi-Fi
> it runs into the download limit (`toomanyrequests`).

All versions: [Releases](https://github.com/marcdon2002/kv-lab/releases/latest)

## Setup

**What you need:** a laptop with Windows 10/11 or macOS, **admin rights** and about **6 GB free disk space**.

| Your laptop | Guide | Takes about |
| --- | --- | --- |
| Windows | [SETUP_WINDOWS.md](./SETUP_WINDOWS.md) | 15–25 min, including a possible restart |
| macOS | [SETUP_MAC.md](./SETUP_MAC.md) | 10–15 min |

Both guides follow the same three steps:

1. **Unzip the kit** to `C:\kv-lab` (Windows) or `~/kv-lab` (macOS). Don't put it in a OneDrive or iCloud folder.
2. **Install Docker Desktop.** On Windows, set up WSL 2 first.
3. **Start Docker Desktop** and wait until it shows **Engine running**.

<details>
<summary>What gets installed?</summary>

| Component | Where it comes from | Size |
| --- | --- | --- |
| Docker Desktop | [docker.com](https://www.docker.com/products/docker-desktop/) | about 0.5–0.6 GB download |
| WSL 2 (Windows only) | Windows itself, `wsl --install --no-distribution` | small, may need a restart |
| Redis 7.4.7 image | `images.tar.gz` in the kit | included, offline |
| Python 3.12 lab image with the demos | `images.tar.gz` in the kit | included, offline |

Nothing is installed directly on your system apart from Docker Desktop and WSL.

</details>

## Lab start

Open a terminal in the `kv-lab` folder. Use **PowerShell** on Windows and **Terminal** on macOS:

```sh
docker load -i images.tar.gz
docker compose up -d --wait
docker compose run --rm lab check
```

`docker load` installs the Redis and lab images from the kit file, without internet. `docker compose up` starts Redis in the background. `check` connects to Redis and tests reading and writing. When everything works, you'll see:

```text
✓ READY – your setup works. See you in the lab!
```

> [!IMPORTANT]
> Run the commands **inside the `kv-lab` folder**: `cd C:\kv-lab` on Windows, `cd ~/kv-lab` on macOS.
> And always run `docker load` before the first `docker compose up`. Otherwise Docker tries to download the images.

## Demos and exercises

| Command | What happens |
| --- | --- |
| `docker compose run --rm lab 1` | **Demo 1 – Keys & TTL:** a login session expires |
| `docker compose run --rm lab 2` | **Demo 2 – Data structures:** profile, visitors, job queue, leaderboard |
| `docker compose run --rm lab 3` | **Demo 3 – Cache-aside:** a cache serves a stale room number |
| `docker compose run --rm lab 4` | **Demo 4 – Atomicity:** a lost update, and how `INCR` fixes it |
| `docker compose exec redis redis-cli` | Type Redis commands yourself (for the exercises) |
| `docker compose run --rm lab reset` | Delete all lab data and start fresh |
| `docker compose down` | Stop the lab |

The demos stop at every **? Predict** question. Think about the answer first, then press **Enter**.
`--no-pause` runs a demo without stopping, e.g. `docker compose run --rm lab 2 --no-pause`.

The exercises with a command cheat sheet are in **[EXERCISES.md](./EXERCISES.md)**.

## What's in the kit

```text
kv-lab/
├── README.md           This overview
├── SETUP_WINDOWS.md    Step-by-step setup for Windows
├── SETUP_MAC.md        Step-by-step setup for macOS
├── EXERCISES.md        Exercises 1–3, bonus tasks and cheat sheet
├── compose.yaml        Redis server and lab container
├── images.tar.gz       Docker images for offline use (only in the release ZIPs)
└── lab/
    ├── Dockerfile      Python 3.12 image with the Redis client
    └── demos.py        Setup check, demos 1–4 and reset
```

<details>
<summary>How the lab works</summary>

- `compose.yaml` defines two services. `redis` runs Redis 7.4.7 **without persistence**, so a restart always starts empty. `lab` runs `demos.py` and is only started on demand with `docker compose run`.
- Redis publishes **no port** on your laptop. The demos and `redis-cli` reach it inside the Docker network. That's why the lab doesn't clash with a Redis you may already have installed.
- All demo keys start with `campus:`, and your own keys in the exercises with `ex:`. `reset` deletes all `campus:*` keys.
- Nothing leaves your laptop. The lab needs no account and no cloud service.

</details>

## Cleaning up

```sh
docker compose down --rmi all
```

This stops the lab and deletes both images, about 400 MB. After that you can uninstall Docker Desktop if you no longer need it.

## Help

The most common problems:

| Message | Fix |
| --- | --- |
| `Cannot connect to the Docker daemon` / `error during connect` | Docker Desktop isn't running. Start it and wait for **Engine running**. |
| `toomanyrequests` / `pull access denied` | `docker load -i images.tar.gz` was skipped. Run it, then try again. |
| `no such file or directory: images.tar.gz` | Wrong folder. First `cd C:\kv-lab` or `cd ~/kv-lab`. |
| Virtualization disabled, no admin rights | Docker can't run on this laptop. Team up with a neighbour. |

More solutions are at the end of the [Windows](./SETUP_WINDOWS.md#troubleshooting) and [macOS](./SETUP_MAC.md#troubleshooting) guides.
**In the lecture:** raise your hand. If you're stuck for more than a minute, team up with your neighbour.

| Topic | Documentation |
| --- | --- |
| Redis commands and data types | [Redis docs](https://redis.io/docs/latest/develop/data-types/) |
| Docker Desktop | [Install on Windows](https://docs.docker.com/desktop/setup/install/windows-install/), [Install on Mac](https://docs.docker.com/desktop/setup/install/mac-install/) |
| Docker Compose | [Compose docs](https://docs.docker.com/compose/) |

**Maintained by** Group 2 · Database Technologies · Hochschule Aalen.
Redis 7.4.7 is distributed under its own licence (RSALv2/SSPLv1). The image is the unmodified official `redis:7.4.7` from Docker Hub.
