import os
import subprocess
from pathlib import Path

def open_folder_or_app(item_name):
    item_name = item_name.strip().lower()

    # Special folders mapping
    special_folders = {
        "downloads": str(Path.home() / "Downloads"),
        "download": str(Path.home() / "Downloads"),
        "pictures": str(Path.home() / "Pictures"),
        "picture": str(Path.home() / "Pictures"),
        "desktop": str(Path.home() / "Desktop"),
        "documents": str(Path.home() / "Documents"),
        "document": str(Path.home() / "Documents"),
        "videos": str(Path.home() / "Videos"),
        "video": str(Path.home() / "Videos"),
        "music": str(Path.home() / "Music"),
        "musics": str(Path.home() / "Music"),
    }

    # Apps mapping (Office 2013 + Snipping Tool)
    apps = {
        "word": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\Word 2013.lnk",
        "microsoft word": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\Word 2013.lnk",
        "excel": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\Excel 2013.lnk",
        "microsoft excel": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\Excel 2013.lnk",
        "powerpoint": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\PowerPoint 2013.lnk",
        "microsoft powerpoint": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Microsoft Office 2013\PowerPoint 2013.lnk",
        "snipping tool": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Accessories\Snipping Tool.lnk",
        "notepad": "notepad.exe",
        "calculator": "calc.exe"
    }

    # Handle drives like "D drive"
    if "drive" in item_name:
        drive_letter = item_name[0].upper()
        drive_path = f"{drive_letter}:\\"
        if os.path.exists(drive_path):
            subprocess.Popen(['explorer', drive_path])
            return f"Opening {drive_letter} drive"
        else:
            return f"{drive_letter} drive not found"

    # Handle special folders
    if item_name in special_folders:
        folder_path = special_folders[item_name]
        if os.path.exists(folder_path):
            subprocess.Popen(['explorer', folder_path])
            return f"Opening {item_name} folder"
        else:
            return f"{item_name} folder not found"

    # Handle apps
    if item_name in apps:
        app_path = apps[item_name]
        if os.path.exists(app_path) or app_path.endswith(".exe"):
            try:
                subprocess.Popen(app_path, shell=True)
                return f"Opening {item_name}"
            except Exception as e:
                return f"Could not open {item_name}: {e}"
        else:
            return f"{item_name} application not found"

    return f"I couldn't recognise or find '{item_name}'"
