# Setup on macOS – in the session

We start at **minute 3**. The download and the installation run while you listen to the theory.

## Part A · Install (minute 3, runs in the background)

### A1 · Which chip do I have? (10 seconds)

*Apple menu → About This Mac*
- **Chip: Apple M1/M2/M3/M4 …** → Apple silicon → `arm64`
- **Processor: Intel …** → Intel → `amd64`

Docker Desktop supports the current macOS and the two previous major versions.
Older macOS → team up with a neighbour.

### A2 · Start the downloads

1. **Docker Desktop:** <https://www.docker.com/products/docker-desktop/>
   → **Download for Mac – Apple Silicon** or **Mac – Intel Chip**
2. **Lab kit:** <https://github.com/marcdon2002/kv-lab/releases/latest>
   - Apple silicon → **`kv-lab-arm64.zip`**
   - Intel → **`kv-lab-amd64.zip`**

   Slow Wi-Fi? Ask for a USB stick.

### A3 · Install Docker Desktop

1. Open the `.dmg` and drag **Docker** into **Applications**
2. Start **Docker** from *Applications* and accept the terms. Enter your password if macOS asks for it
   (Docker installs a helper). Docker Desktop is free for personal and education use. You can **skip** signing in.
3. Wait until Docker Desktop shows **Engine running**

### A4 · Unzip the kit

Double-click the ZIP and move the `kv-lab` folder into your **home folder**, so it is at `~/kv-lab`.

**Not inside iCloud Drive or OneDrive.**

✅ **Checkpoint (minute 34):** Docker Desktop shows *Engine running* and `~/kv-lab` exists.

## Part B · Lab start (minute 48)

Open **Terminal** (*Applications → Utilities → Terminal*):

```bash
cd ~/kv-lab
docker load -i images.tar.gz
docker compose up -d --wait
docker compose run --rm lab check
```

You should see:

```
✓ READY – your setup works. See you in the lab!
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Cannot connect to the Docker daemon at unix:///…/docker.sock` | Docker Desktop is not running. Start it and wait for **Engine running**. |
| `zsh: command not found: docker` | Start Docker Desktop once, then open a new Terminal window. |
| Docker Desktop won't start / "not supported" | Wrong download (Intel vs. Apple silicon) or macOS too old. Check A1. |
| `toomanyrequests` or `pull access denied` | `docker load -i images.tar.gz` was skipped. Run it, then try again. |
| `open images.tar.gz: no such file or directory` | Wrong folder. Run `cd ~/kv-lab` first (or `cd ~/Downloads/kv-lab`). |
| Warning `platform (linux/amd64) does not match` | You took the wrong kit. Apple chip → `kv-lab-arm64.zip`. It still works, just slower. |
| Anything else for more than 1 minute | Raise your hand – or team up with a neighbour. |
