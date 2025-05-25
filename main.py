# ============================================
# SnapBox - Automated screen capture and Telegram delivery
# Author: Adrian Anghel
# Company: Matei Conf Grup S.R.L.
# Version: v1.0.0
# Release Date: 2025-05-22
# Contact: it@mateiconfgrup.ro
# ============================================


import time, threading, datetime, io, os, ctypes
import requests
import win32gui, win32con, win32process
from PIL import ImageGrab
from config import *


# Determine base path for logs (supports both .py and .exe)
import sys
if getattr(sys, 'frozen', False):
    base_path = os.path.dirname(sys.executable)
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

log_file_path = os.path.join(base_path, "log.txt")

# Write to log.txt
def log(msg):
    with open(log_file_path, "a", encoding="utf-8") as f:
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        f.write(f"{timestamp} {EBOX_NAME}: {msg}\n")

# Truncate log if it exceeds max size
def truncate_log(max_size_mb=5, keep_lines=100):
    if os.path.exists(log_file_path):
        if os.path.getsize(log_file_path) > max_size_mb * 1024 * 1024:
            try:
                with open(log_file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                last_lines = lines[-keep_lines:]
                with open(log_file_path, "w", encoding="utf-8") as f:
                    f.write("[LOG TRUNCATED – last 100 lines kept]\n")
                    f.writelines(last_lines)
                log(f"[AUTO-TRUNCATED LOG] Kept last {keep_lines} lines.")
            except Exception as e:
                log(f"Log truncation error: {e}")

# Get window handle by title
def get_hwnd(title_substring):
    hwnds = []
    def enum_handler(hwnd, _):
        if win32gui.IsWindowVisible(hwnd) and title_substring.lower() in win32gui.GetWindowText(hwnd).lower():
            hwnds.append(hwnd)
    win32gui.EnumWindows(enum_handler, None)
    return hwnds[0] if hwnds else None

# Force focus on a window
def force_focus_window(hwnd):
    try:
        foreground_hwnd = win32gui.GetForegroundWindow()
        current_thread = win32process.GetWindowThreadProcessId(foreground_hwnd)[0]
        target_thread = win32process.GetWindowThreadProcessId(hwnd)[0]
        ctypes.windll.user32.AttachThreadInput(current_thread, target_thread, True)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        win32gui.BringWindowToTop(hwnd)
        win32gui.SetForegroundWindow(hwnd)
        ctypes.windll.user32.AttachThreadInput(current_thread, target_thread, False)
        log(f"Focus on: {win32gui.GetWindowText(hwnd)}")
        return True
    except Exception as e:
        log(f"Focus error: {e}")
        return False

# Capture full screen
def capture_fullscreen():
    try:
        img = ImageGrab.grab()
        output = io.BytesIO()
        img.save(output, format="PNG")
        output.seek(0)
        return output
    except Exception as e:
        log(f"Capture error: {e}")
        return None

# Send screenshot to Telegram
def send_photo(image_bytes, chat_id, caption):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
        files = {"photo": ("screen.png", image_bytes)}
        data = {"chat_id": chat_id, "caption": caption}
        response = requests.post(url, files=files, data=data)
        if response.status_code == 200:
            log(f"Sent: {caption}")
        else:
            log(f"Send error: {response.status_code} - {response.text}")
    except Exception as e:
        log(f"HTTP error: {e}")

# Switch window, capture and optionally return to AIRPORT
def switch_and_capture(window_title, chat_id, label, return_to_airport=True):
    hwnd_target = get_hwnd(window_title)
    hwnd_airport = get_hwnd(AIRPORT_WINDOW_TITLE)
    if hwnd_target:
        force_focus_window(hwnd_target)
        time.sleep(2)
        img = capture_fullscreen()
        if img:
            send_photo(img, chat_id, f"{label} – {EBOX_NAME}")
        else:
            log("Capture failed.")
        if return_to_airport and hwnd_airport:
            force_focus_window(hwnd_airport)
    else:
        log(f"Window not found: {window_title}")

# Automatic capture loop
def periodic_task():
    log("Automatic capture running.")
    last_sent_plc = None
    last_sent_airport = None

    while True:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.weekday()

        in_active_hours = (
            ACTIVE_HOURS["start"] <= current_time <= ACTIVE_HOURS["end"] and
            current_day in ACTIVE_HOURS["days"]
        )

        if in_active_hours:
            if (not last_sent_plc or
                (now - last_sent_plc).total_seconds() >= CAPTURE_INTERVAL_PLC_MINUTES * 60):
                log("Automatic PLC capture")
                switch_and_capture(PLC_WINDOW_TITLE, CHAT_ID_PLC, "PLC Capture", return_to_airport=False)
                last_sent_plc = now

            if (not last_sent_airport or
                (now - last_sent_airport).total_seconds() >= CAPTURE_INTERVAL_AIRPORT_MINUTES * 60):
                hwnd_airport = get_hwnd(AIRPORT_WINDOW_TITLE)
                if hwnd_airport:
                    force_focus_window(hwnd_airport)
                    time.sleep(1)
                log("Automatic Airport capture")
                switch_and_capture(AIRPORT_WINDOW_TITLE, CHAT_ID_AIRPORT, "Airport Capture", return_to_airport=False)
                last_sent_airport = now
        else:
            log("Outside active hours.")
        time.sleep(5)

# Handle manual Telegram commands
def listen_for_commands():
    log("Listening for Telegram commands...")
    offset = None
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
            if offset:
                url += f"?offset={offset+1}"
            r = requests.get(url, timeout=10).json()
            for update in r.get("result", []):
                offset = update["update_id"]
                msg = update.get("message", {})
                text = msg.get("text", "")
                chat_id = msg.get("chat", {}).get("id")
                if str(chat_id) != str(CHAT_ID_COMMANDS):
                    continue
                line = text.strip().lower()
                if line.startswith("/plc") or line.startswith("/airport"):
                    try:
                        cmd, target = line.split(maxsplit=1)
                        normalized_target = target.replace("-", "").replace(" ", "").lower()
                        normalized_ebox = EBOX_NAME.replace("-", "").replace(" ", "").lower()

                        if target == "all" or normalized_target == normalized_ebox:
                            if cmd == "/plc":
                                log(f"Manual command: /plc {target}")
                                switch_and_capture(PLC_WINDOW_TITLE, chat_id, "PLC Request")
                            elif cmd == "/airport":
                                log(f"Manual command: /airport {target}")
                                switch_and_capture(AIRPORT_WINDOW_TITLE, chat_id, "Airport Request", return_to_airport=False)
                    except ValueError:
                        log("Invalid command: missing argument.")
        except Exception as e:
            log(f"Command handler error: {e}")
        time.sleep(2)

# Application entry point
if __name__ == "__main__":
    truncate_log()
    log("Script started.")
    threading.Thread(target=listen_for_commands, daemon=True).start()
    periodic_task()
