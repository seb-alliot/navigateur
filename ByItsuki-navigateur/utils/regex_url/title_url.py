from urllib.parse import urlparse, parse_qs, unquote

def site_name(web_view_title, moteur):
    print(f"site_name appelé avec: {web_view_title}, moteur: {moteur}")

    parsed_url = urlparse(web_view_title)
    query_params = parse_qs(parsed_url.query)

    # Définition des suffixes à enlever
    suffixes = (" - Recherche Google", " - Google Search", " - Bing", " at DuckDuckGo", " – Recherche Qwant", " - Recherche")

    # Extraction du param 'q' si présent
    search_term = web_view_title
    if 'q' in query_params:
        search_term = unquote(query_params['q'][0])

    # Nettoyage des suffixes
    for s in suffixes:
        if s in search_term:
            search_term = search_term.replace(s, '')

    return search_term.strip()
