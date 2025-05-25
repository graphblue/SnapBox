# SnapBox – Full Installation Guide v1.0

## 0. Optional – Download SnapBox using Git

If you prefer to automatically retrieve the latest version of SnapBox from GitHub instead of manually downloading ZIP files:

### ✅ Step-by-step

1. Download and install **Git for Windows** from: https://git-scm.com/download/win

2. Open **Command Prompt** or **Git Bash** and run:

```bash
git clone https://github.com/graphblue/SnapBox.git C:\SnapBox
```

3. Navigate into the folder:

```cmd
cd C:\SnapBox
```

4. If you need to update later:

```bash
git pull origin main
```

> This method will ensure your installation stays synchronized with official releases.

---

## 1. Create the Telegram Bot

- Open [@BotFather](https://t.me/BotFather) in Telegram
- Type `/newbot` and follow the steps to choose a name and username
- At the end, you'll receive a **BOT TOKEN** – keep it for `config.py`

---

## 2. Create Group and Private Channels

- Create a private group (e.g., **MCG PMS**) – this will be used for manual commands
- Create two **private channels**:
  - `MCG_Plc` – for PLC screenshots
  - `MCG_Airport` – for Airport screenshots
- Add the bot as **admin** in the group and both channels
- Go to `@BotFather > /mybots > Settings > Group Privacy > Turn off`

---

## 3. Identify Telegram Chat IDs (private method)

- Send a message in the group and each private channel
- Right-click / long-tap on the message → **Copy message link**
- From the link `https://t.me/c/2657536428/12`, extract the numeric ID after `/c/`
- Prefix with `-100` → becomes `-1002657536428`
- Add to `config.py` as:

```python
CHAT_ID_PLC = "-1002657536428"
CHAT_ID_AIRPORT = "-1002542193205"
CHAT_ID_COMMANDS = "-1002504925466"
```

---

## 4. Install Python

- Run the installer: `python-3.x.x.exe`
- Check **“Add Python to PATH”**
- Click **Install Now**

---

## 5. Install Required Libraries

- Run the batch script:
```bat
install_requirements_snapbox.bat
```

- This installs:
  - `pillow`
  - `requests`
  - `pywin32`
  - `pyinstaller`

---

## 6. Configure `config.py`

- Open `config.py` in Notepad
- Fill in the fields below:

```python
EBOX_NAME = "E-Box MC3"
BOT_TOKEN = "<your BotFather token>"
CHAT_ID_PLC = "-100XXXXXXXXXX"
CHAT_ID_AIRPORT = "-100XXXXXXXXXX"
CHAT_ID_COMMANDS = "-100XXXXXXXXXX"
```

- Schedule and frequency:

```python
ACTIVE_HOURS = {
    "start": "07:00",
    "end": "15:30",
    "days": [0, 1, 2, 3, 4]  # Monday to Friday
}

CAPTURE_INTERVAL_PLC_MINUTES = 30
CAPTURE_INTERVAL_AIRPORT_MINUTES = 15
```

---

## 7. Compile the Executable

- Run:
```bat
build_snapbox.bat
```

- Result: `SnapBox.exe` will be in the `dist/` folder

---

## 8. Task Scheduler Setup

- Open **Task Scheduler**
- Click **“Import Task…”**, choose `task_scheduler_snapbox.xml`
- Confirm path to: `start_snapbox.bat`
- Configure:
  - Trigger: **At user logon**
  - Security: **Run with highest privileges**

---

## 9. Final Test

- Run: `start_snapbox.bat`
- From Telegram group, send:

```
/plc all
/plc E-Box MC1
/plc E-Box MC2
/plc E-Box MC3
```

- Confirm:
  - Screenshots are delivered to proper channels
  - `log.txt` is updated in `C:\SnapBox\dist`