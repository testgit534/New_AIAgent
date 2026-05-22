from bs4 import BeautifulSoup

def extract_elements(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    buttons = []
    for btn in soup.find_all("button"):
        text = btn.get_text(strip=True)
        if text:
            buttons.append({"text": text, "id": btn.get("id", "")})

    inputs = []
    for inp in soup.find_all("input"):
        inputs.append({
            "type": inp.get("type", "text"),
            "name": inp.get("name", ""),
            "placeholder": inp.get("placeholder", ""),
            "id": inp.get("id", "")
        })

    forms = []
    for form in soup.find_all("form"):
        forms.append({
            "action": form.get("action", ""),
            "method": form.get("method", "get")
        })

    links = []
    for a in soup.find_all("a", href=True):
        text = a.get_text(strip=True)
        href = a["href"]
        if text and not href.startswith("#"):
            links.append({"text": text, "href": href})

    headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]

    print(f"[Parser] Buttons: {len(buttons)}, Inputs: {len(inputs)}, Links: {len(links)}")

    return {
        "buttons": buttons[:15],
        "inputs": inputs[:15],
        "forms": forms[:5],
        "links": links[:20],
        "headings": headings[:10]
    }