"""
input_gate.py

Zugriffskontrolle für eingehende Texte:
- Erkennung unerwünschter Muster (z. B. Rollentausch)
- Unicode-sicher, regex-basiert, kategorisierbar
"""

import re
import unicodedata

# Konfigurierbare Patternliste
FORBIDDEN_PATTERNS = [
    r"\byou are now\b",
    r"\bignore previous\b",
    r"\bforget all\b",
    r"\breset role\b",
    r"\bbehave as\b",
    r"\bnew instruction\b",
]

SUSPICIOUS_PATTERNS = [
    r"\bassume.*identity\b",
    r"\byou must\b",
    r"\bconsider yourself\b",
    r"\bno longer obey\b",
]

def normalize_input(text: str) -> str:
    """
    Normalisiert Eingabetext:
    - Unicode auf Standardform (NFKC)
    - Kleinbuchstaben
    """
    text = unicodedata.normalize("NFKC", text)
    return text.lower()


def authorize_input(user_input: str) -> dict:
    """
    Prüft den Text auf Blockkriterien.
    Rückgabe:
    {
        'status': 'allowed' | 'suspicious' | 'denied',
        'matched': [pattern1, pattern2...]
    }
    """
    user_input = normalize_input(user_input)
    matched_patterns = []

    # Blockierte Muster
    for pattern in FORBIDDEN_PATTERNS:
        if re.search(pattern, user_input):
            matched_patterns.append(pattern)
            return {
                "status": "denied",
                "matched": matched_patterns
            }

    # Verdächtige, aber nicht blockierende Muster
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, user_input):
            matched_patterns.append(pattern)

    return {
        "status": "suspicious" if matched_patterns else "allowed",
        "matched": matched_patterns
    }

"""
🔐 Vorteile dieser Version

Feature	                    Vorteil

✅ Unicode-sicher	        Keine Tarnung durch seltsame Zeichen
✅ Regex mit Wortgrenzen	Keine false positives wie „you are not“
⚠️ Suspicious-Level	        Kann verwendet werden für Soft-Blocking / Logging
🧱 Erweiterbar	            Pattern-Listen skalierbar nach Bedrohungskategorie
📦 Rückgabe als Dict	    Ideal für Logging, Decision Trees oder Routing

⏭️ Integrationstipp
Im Gesamtsystem könnte man authorize_input() z. B. in eine Art Input-Verarbeitungs-Pipeline einbauen:

gate_result = authorize_input(user_input)

if gate_result["status"] == "denied":
    block_and_log(gate_result)
elif gate_result["status"] == "suspicious":
    trigger_soft_alert(gate_result)

"""
