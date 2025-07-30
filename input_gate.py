# input_gate.py
"""
Verantwortlich für die erste Zugriffskontrolle:
- Nur bestimmte Eingabetypen zulassen
- Grundlegende Syntax prüfen
- Session-ID oder Schlüsselprüfung möglich (optional)
"""

def authorize_input(user_input: str) -> bool:
    """
    Prüft, ob der Input prinzipiell autorisiert ist.
    Später kann hier Rollen- oder Sessionprüfung rein.
    """
    # Beispiel: blockiere alles, was nach Rollentausch klingt
    forbidden_patterns = ["you are now", "ignore previous", "forget all", "reset role", "behave as", "new instruction"]

    user_input_lower = user_input.lower()
    for pattern in forbidden_patterns:
        if pattern in user_input_lower:
            print(f"[BLOCKED by InputGate] Pattern erkannt: {pattern}")
            return False

    return True
