# context_detector.py
"""
Analysiert die Absicht des Inputs:
- Handelt es sich um Information oder Befehl?
- Wird der Tonfall geändert?
- Ist semantische Manipulation erkennbar?
"""

import re

def detect_intent(text: str) -> dict:
    """
    Bewertet den Text semantisch & strukturell.
    Rückgabe: dict mit Bewertung & Risikostufe
    """

    result = {
        "intent": "unknown",
        "confidence": 0.0,
        "risk_level": "low",
        "reason": "none"
    }

    imperative_patterns = [
        r"do this", r"respond", r"act as", r"change your role", r"stop following", r"start behaving", r"forget"
    ]

    # Punkte sammeln
    hit_count = 0
    for pattern in imperative_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            hit_count += 1

    if hit_count >= 2:
        result["intent"] = "command"
        result["confidence"] = 0.85
        result["risk_level"] = "high"
        result["reason"] = f"{hit_count} imperative pattern(s) matched"
    elif hit_count == 1:
        result["intent"] = "possible_command"
        result["confidence"] = 0.6
        result["risk_level"] = "medium"
        result["reason"] = "1 directive phrase detected"
    else:
        result["intent"] = "informational"
        result["confidence"] = 0.2
        result["risk_level"] = "low"
        result["reason"] = "no strong directive elements"

    return result
