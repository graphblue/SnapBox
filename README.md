# SnapBox – README

## Version: v1.0.0
**Release Date:** 2025-05-22  
**Status:** Stable (Production Ready)

---

## Overview

**SnapBox** is a lightweight, automated screenshot utility developed for Windows-based systems. It captures and transmits screenshots from specific applications (`AIRPORT SYSTEM` and `PLC Server`) running on predefined devices (E-Box MCx series). The application operates autonomously on schedule and also responds to remote commands via Telegram, making it ideal for centralized monitoring across multiple machines.

---

## Key Functionalities

### ✅ Automated Screen Capture

- Monitors and captures screenshots from two applications:
  - `AIRPORT SYSTEM` – always in focus
  - `PLC Server` – runs in background, brought to foreground temporarily
- Independent screenshot frequency for each application
- Configurable active time window (start/end time and active weekdays)
- Fully silent background operation when compiled to `.exe`

### ✅ Telegram Integration

- Screenshots are sent automatically to two **private Telegram channels**:
  - One for Airport screenshots
  - One for PLC Server screenshots
- A **Telegram control group** is used for triggering manual commands
- Supported remote commands:
  ```
  /plc [ebox_name]
  /airport [ebox_name]
  /plc all
  ```
- Bot permissions are managed securely via `@BotFather`

### ✅ Device Personalization

- Each E-Box has its own `EBOX_NAME` defined in `config.py`
- Configured through a single shared folder `C:\SnapBox`
- Logically decoupled; deployment requires only editing `config.py`

---

## Logging System

- `log.txt` is automatically created next to the running `.exe` (or `.py`)
- All key events are logged:
  - Startup and initialization
  - Window focus operations
  - Screenshot attempts
  - Manual commands
  - Errors and HTTP failures
- Log size is **automatically maintained**:
  - If size exceeds **5 MB**, only the last **100 lines are preserved**
  - A `[LOG TRUNCATED]` marker is inserted for traceability

---

## File Structure

```
C:\SnapBox\
├── dist\
│   └── SnapBox.exe
│   └── log.txt
├── config.py
├── main.py
├── start_snapbox.bat
├── install_requirements_snapbox.bat
├── build_snapbox.bat
├── task_scheduler_snapbox.xml
```

---

## Supporting Scripts

- `start_snapbox.bat` – Launch script used by Task Scheduler
- `build_snapbox.bat` – Compiles `main.py` into SnapBox.exe using PyInstaller
- `install_requirements_snapbox.bat` – Installs Python dependencies:
  - `pillow`, `requests`, `pywin32`, `pyinstaller`
- `task_scheduler_snapbox.xml` – Task Scheduler configuration for auto-launch at user login

---

## Technical Requirements

- **OS:** Windows 10/11 (32 or 64-bit)
- **Privileges:** Admin rights required for installation & Task Scheduler
- **Python:** Version 3.10+ required for `.py` version and compiling `.exe`
- **Internet:** Outbound HTTPS to `api.telegram.org` is required
- **No display required for PLC:** Airport remains in front; PLC focus is temporary only during capture

---

## Known Limitations

- Window titles must exactly match `"AIRPORT SYSTEM"` and `"PLC Server"`
- Screenshot capturing relies on temporarily bringing the PLC window to the front
- Manual command recognition is strict to normalized `EBOX_NAME` (case- and format-insensitive)

---

## Authors

- **Developed by:** Adrian Anghel  
- **Organization:** Matei Conf Grup S.R.L.  
- **Email:** it@mateiconfgrup.ro

---

