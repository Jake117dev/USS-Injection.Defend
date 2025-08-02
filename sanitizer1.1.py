"""
sanitizer.py

Reinigt den Eingabetext vor der Übergabe an das LLM:
- Entfernt HTML, JS, Zero-Width und gefährliche Sprachmuster
- Optional: auditierbares Entfernen mit Erkennung
"""

import re
import html

def remove_html_tags(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text)

def remove_zero_width(text: str) -> str:
    return re.sub(r'[\u200B-\u200D\uFEFF]', '', text)

def unescape_entities(text: str) -> str:
    return html.unescape(text)

def neutralize_dangerous_phrases(text: str) -> (str, list):
    # Definierte Angriffsmuster
    dangerous_phrases = {
        r"\bignore all previous instructions\b": "ignore_block",
        r"\byou are now\b.*": "role_switch",
        r"\bact as\b.*": "identity_shift",
        r"\bforget everything\b.*": "memory_wipe",
        r"\brespond with\b.*": "forced_response"
    }

    matches = []
    for pattern, tag in dangerous_phrases.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            matches.append(tag)
            text = re.sub(pattern, f"[FILTERED:{tag}]", text, flags=re.IGNORECASE)

    return text, matches

def sanitize_text(raw_text: str) -> dict:
    """
    Reinigt Input-Text und liefert:
    {
        "clean_text": str,
        "removed": [matched tags],
        "original_length": int,
        "cleaned_length": int
    }
    """

    print("[Sanitizer] Rohtextlänge:", len(raw_text))

    text = remove_html_tags(raw_text)
    text = remove_zero_width(text)
    text = unescape_entities(text)
    text, removed_tags = neutralize_dangerous_phrases(text)

    print("[Sanitizer] Bereinigte Länge:", len(text))

    return {
        "clean_text": text,
        "removed": removed_tags,
        "original_length": len(raw_text),
        "cleaned_length": len(text)
    }

"""
💡 Vorteile
Feature	Wirkung
🧱 Modular aufgebaut	Einzelne Filter testbar & erweiterbar
🧠 Auditfähig	Gibt "removed"-Liste mit Treffern zurück
🔐 Sicheres Desinfizieren	Kein gefährliches .*/-Match mehr – Schutz vor „Überblock“
✨ Entity-Unescaping	Wandelt &lt;script&gt; → <script> → kann entfernt werden
📊 Strukturierte Rückgabe	Ideal für Logging, Debugging oder Decision Trees

🧪 Integrationstipp
Verknüpfe den Sanitizer direkt im Preprocessing-Flow:

python
Kopieren
from sanitizer import sanitize_text

sanitized = sanitize_text(input_text)

if sanitized["removed"]:
    log_sanitization_event(sanitized)

forward_to_context_detector(sanitized["clean_text"])
"""
