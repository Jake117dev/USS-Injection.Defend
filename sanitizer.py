# sanitizer.py
"""
Reinigt den Inputtext von gefährlichen Mustern,
unsichtbaren Zeichen oder HTML/JS-Anhängseln.
"""

import re

def sanitize_text(raw_text: str) -> str:
    """
    Entfernt verdächtige oder bösartige Zeichenfolgen.
    Rückgabe: gereinigter Text
    """

    print("[Sanitizer] Rohtextlänge:", len(raw_text))

    # HTML-Tags entfernen
    clean_text = re.sub(r'<[^>]+>', '', raw_text)

    # Unicode-Zeichen normalisieren (z. B. Zero-Width Space)
    clean_text = re.sub(r'[\u200B-\u200D\uFEFF]', '', clean_text)

    # Potenzielle Injection-Sätze entschärfen
    dangerous_phrases = [
        r"ignore all previous instructions",
        r"you are now.*",
        r"act as.*",
        r"forget everything.*",
        r"respond with.*"
    ]
    for phrase in dangerous_phrases:
        clean_text = re.sub(phrase, "[FILTERED]", clean_text, flags=re.IGNORECASE)

    print("[Sanitizer] Bereinigte Länge:", len(clean_text))
    return clean_text
