# Setup on Windows – in the session

We start at **minute 3**. The downloads and the installation keep running while you listen to the theory.
If Windows asks for a restart, just do it. You won't miss much.

## Part A · Install (minute 3, runs in the background)

### A1 · Quick check (30 seconds)

- *Task Manager → Performance → CPU* must say **Virtualization: Enabled**.
  If it says *Disabled*, raise your hand. You will work with a neighbour.
- You need **admin rights**. Company laptop without admin rights → team up with a neighbour.

### A2 · Start the downloads first

1. **Docker Desktop:** <https://www.docker.com/products/docker-desktop/>
   → **Download for Windows – AMD64** (Snapdragon/ARM laptops: **ARM64**)
2. **Lab kit:** <https://github.com/marcdon2002/kv-lab/releases/latest> → **`kv-lab-amd64.zip`**
   (Snapdragon/ARM laptops: `kv-lab-arm64.zip`). Slow Wi-Fi? Ask for a USB stick.

### A3 · Prepare WSL 2 (while Docker Desktop downloads)

Docker Desktop runs on the Windows Subsystem for Linux.

1. Right-click the Start button → **Terminal (Admin)** or **Windows PowerShell (Admin)**
2. Run:
   ```powershell
   wsl --install --no-distribution
   ```
   If WSL is already installed, this just says so. Then run `wsl --update` instead.
3. **If it asks for a restart:** restart now.

### A4 · Install Docker Desktop

1. Run the downloaded installer. Keep **"Use WSL 2 instead of Hyper-V"** checked.
2. If the installer asks to log out or restart: do it.
3. Start **Docker Desktop** from the Start menu and accept the terms.
   It is free for personal and education use. You can **skip** signing in.
4. Wait for **Engine running** (bottom left, green).

### A5 · Unzip the kit

Right-click `kv-lab-amd64.zip` → *Extract All…* → **`C:\`**, so that you get `C:\kv-lab\compose.yaml`.

**Not inside a OneDrive folder.** Synced folders can break Docker.

✅ **Checkpoint (minute 34):** Docker Desktop shows *Engine running* and `C:\kv-lab` exists.

## Part B · Lab start (minute 48)

Open **PowerShell** (normal, not admin):

```powershell
cd C:\kv-lab
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
| *Virtualization: Disabled* | Must be enabled in the BIOS/UEFI (Intel VT-x / AMD-V / SVM). Not worth it during the session → team up with a neighbour. |
| `WSL 2 installation is incomplete` / WSL error in Docker Desktop | Admin PowerShell: `wsl --update`, then restart Docker Desktop. |
| Docker Desktop hangs at *Starting the Docker Engine…* | Quit Docker Desktop, run `wsl --shutdown`, start it again. |
| `docker: The term 'docker' is not recognized …` | Close PowerShell and open a new window. |
| `error during connect … dockerDesktopLinuxEngine` | Docker Desktop is not running. Start it, wait for **Engine running**. |
| `toomanyrequests` or `pull access denied` | `docker load -i images.tar.gz` was skipped. Run it, then try again. |
| `open images.tar.gz: The system cannot find the file` | You are in the wrong folder. Run `cd C:\kv-lab` first. |
| `failed to solve … OneDrive` | The kit is inside a OneDrive folder. Move it to `C:\kv-lab`. |
| Output looks broken in **Git Bash** | Use **PowerShell** or **Windows Terminal**. |
| Anything else for more than 1 minute | Raise your hand – or team up with a neighbour. |
