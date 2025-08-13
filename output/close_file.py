import os
import psutil
import platform
import subprocess
import pyautogui  # pip install pyautogui
import re
import time

# Synonyms for "close"
CLOSE_KEYWORDS = [
    "close", "exit", "quit", "end", "stop", "terminate",
    "kill", "shut", "shut down", "turn off", "switch off"
]

# Common app name mappings (human name → real process name)
APP_ALIASES = {
    "word": "WINWORD",
    "microsoft word": "WINWORD",
    "excel": "EXCEL",
    "excel sheet": "EXCEL",
    "powerpoint": "POWERPNT",
    "ppt": "POWERPNT",
    "chrome": "chrome",
    "firefox": "firefox",
    "edge": "msedge",
    "notepad": "notepad",
    "calculator": "CalculatorApp"
}

# Common folder keywords
FOLDER_KEYWORDS = [
    "downloads", "documents", "desktop", "pictures", "music", "videos", "folder", "file explorer"
]


def close_application(app_name):
    """Closes an application by name across Windows, macOS, and Linux."""
    app_name = app_name.lower()
    process_name = APP_ALIASES.get(app_name, app_name)

    if platform.system() == "Windows":
        for process in psutil.process_iter(['pid', 'name']):
            try:
                if process_name.lower() in process.info['name'].lower():
                    psutil.Process(process.info['pid']).terminate()
                    return f"Closed {app_name}"
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return f"Could not find {app_name} running."

    elif platform.system() == "Darwin":  # macOS
        try:
            subprocess.call(["osascript", "-e", f'quit app "{app_name.title()}"'])
            return f"Closed {app_name}"
        except Exception as e:
            return f"Error closing {app_name}: {e}"

    elif platform.system() == "Linux":
        try:
            os.system(f"pkill -i -f {process_name}")
            return f"Closed {app_name}"
        except Exception as e:
            return f"Error closing {app_name}: {e}"

    else:
        return "Unsupported OS."


def close_tab_or_window():
    """Closes the current browser tab or file explorer window."""
    if platform.system() == "Darwin":
        pyautogui.hotkey('command', 'w')
    else:
        pyautogui.hotkey('ctrl', 'w')
    return "Closed the current tab or window."


def focus_and_close_folder(folder_name):
    """Attempts to bring the folder window to front before closing."""
    # On Windows, we can use Alt+Tab to cycle through windows
    pyautogui.hotkey('alt', 'tab')
    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'w')
    return f"Closed {folder_name} folder."


def handle_close_command(command):
    """Detects and executes the correct close action with human language support."""
    command = command.lower()

    if not any(keyword in command for keyword in CLOSE_KEYWORDS):
        return "No close command detected."

    # Handle tab closing
    if "tab" in command:
        return close_tab_or_window()

    # Handle folders
    for folder in FOLDER_KEYWORDS:
        if folder in command:
            return focus_and_close_folder(folder)

    # Extract app name after close keyword
    for keyword in CLOSE_KEYWORDS:
        if keyword in command:
            app_name = command.split(keyword, 1)[-1].strip()
            app_name = re.sub(r"^(the\s+)?(app|application|program|software)\s*", "", app_name)
            if app_name:
                return close_application(app_name)

    return "Could not understand what to close."


if __name__ == "__main__":
    print(handle_close_command("shut down excel sheet"))
    print(handle_close_command("kill word"))
    print(handle_close_command("please close my downloads folder"))
    print(handle_close_command("exit chrome tab"))
    print(handle_close_command("terminate ppt presentation"))
