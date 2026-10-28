# Key-Value Databases Lab

Hands-on lab for the *Key-Value Databases* session (Database Technologies, Hochschule Aalen).
You will run a real Redis server on your own laptop and try sessions, caching, leaderboards and atomic updates.

**We install everything together in the session.** You only need to bring:

- a laptop with **Windows 10/11** or **macOS**, fully charged
- **admin rights** on the laptop (needed to install Docker Desktop)
- about **6 GB free disk space**

## The plan

| When in the session | What you do                                                              | Guide |
|---------------------|--------------------------------------------------------------------------|-------|
| **Minute 3 – start**| Download and install **Docker Desktop**, unzip this kit. Installation runs while the theory continues. | [Windows](SETUP_WINDOWS.md) · [macOS](SETUP_MAC.md) |
| **Minute 34 – checkpoint** | Docker Desktop shows **Engine running**?                          | – |
| **Minute 48 – lab start** | Load the lab images from the kit, start Redis, check                 | below |

## Download the kit

| Your laptop                                   | Download                                                                                          |
|-----------------------------------------------|---------------------------------------------------------------------------------------------------|
| Windows (Intel/AMD) · Mac with **Intel** chip | **[kv-lab-amd64.zip](https://github.com/marcdon2002/kv-lab/releases/latest/download/kv-lab-amd64.zip)** |
| Mac with **Apple** chip (M1, M2, M3, M4 …) · Windows on ARM (Snapdragon) | **[kv-lab-arm64.zip](https://github.com/marcdon2002/kv-lab/releases/latest/download/kv-lab-arm64.zip)** |

Not sure? Mac: *Apple menu → About This Mac*. Windows: almost always `amd64`.

All downloads: <https://github.com/marcdon2002/kv-lab/releases/latest>

> **Don't use the green "Code → Download ZIP" button.** It doesn't contain the Docker images (`images.tar.gz`),
> so the lab would try to download them from Docker Hub and fail in the lecture Wi-Fi.

## Lab start (minute 48) – identical on Windows and macOS

Open a terminal (Windows: **PowerShell**, macOS: **Terminal**) in the `kv-lab` folder:

```
docker load -i images.tar.gz
docker compose up -d --wait
docker compose run --rm lab check
```

`docker load` installs Redis and the lab from the kit file. **No internet needed.** When you see this, you're ready:

```
✓ READY – your setup works. See you in the lab!
```

## Commands during the lab

| What                         | Command                                     |
|------------------------------|---------------------------------------------|
| Demo 1 – Keys & TTL          | `docker compose run --rm lab 1`             |
| Demo 2 – Data structures     | `docker compose run --rm lab 2`             |
| Demo 3 – Cache-aside         | `docker compose run --rm lab 3`             |
| Demo 4 – Atomicity           | `docker compose run --rm lab 4`             |
| Type Redis commands yourself | `docker compose exec redis redis-cli`       |
| Delete all lab data          | `docker compose run --rm lab reset`         |
| Stop everything              | `docker compose down`                       |

The demos stop at every **? Predict** question. Think about the answer first, then press **Enter**.
The exercises are in [EXERCISES.md](EXERCISES.md).

## After the lab

```
docker compose down --rmi all
```

This stops the lab and frees the disk space. Then you can uninstall Docker Desktop if you don't need it any more.
