from urllib.parse import urlparse, parse_qs, unquote

def site_name(web_view_title: str, moteur=None) -> str:
    """
    Détermine un nom propre de site ou de recherche à partir du titre et/ou de l'URL.
    Compatible avec Google, Bing, DuckDuckGo, Qwant, etc.
    """
    if not web_view_title:
        return ""

    # --- Si c’est une URL (contient http ou https)
    if web_view_title.startswith("http"):
        parsed_url = urlparse(web_view_title)
        domain = parsed_url.netloc.lower()
        query_params = parse_qs(parsed_url.query)

        # Cas : pages de recherche
        if "google" in domain or "bing" in domain or "duckduckgo" in domain or "qwant" in domain:
            search_term = query_params.get("q", [""])[0]
            if search_term:
                return unquote(search_term).replace("+", " ").strip().capitalize()

        # Cas générique : juste le nom de domaine sans www
        domain = domain.replace("www.", "")
        return domain.split(".")[0].capitalize()

    # --- Sinon, c’est un titre de page classique
    suffixes = (
        " - Recherche Google", " - Google Search", " - Bing",
        " at DuckDuckGo", " – Recherche Qwant", " - Recherche",
    )

    clean_title = web_view_title
    for s in suffixes:
        if s in clean_title:
            clean_title = clean_title.replace(s, "")

    return clean_title.strip().capitalize()
