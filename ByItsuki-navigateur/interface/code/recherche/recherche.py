from PyQt6.QtCore import QUrl

def research(self, query):
    query = query.strip()
    if not query:
        return None

    url = QUrl(f"https://www.google.com/search?q={query}")

    return [url]
