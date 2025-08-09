
import webbrowser

# Dictionary of website commands and their URLs
websites = {
    "youtube": "https://www.youtube.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
    "chatgpt": "https://chat.openai.com",
    "github": "https://github.com",
    "wikipedia": "https://www.wikipedia.org",
    "google classroom": "https://classroom.google.com"
}

def open_website(command):
    command = command.lower()

    for site_name, url in websites.items():
        if site_name in command:
            webbrowser.open(url)
            return f"Opening {site_name.capitalize()}..."
    
    return "Sorry, I don't know that website."

