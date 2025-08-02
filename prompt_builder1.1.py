"""
prompt_builder.py

Erzeugt den finalen Prompt-Kontext zur Übergabe an das LLM:
- Inklusive Schutz vor Strukturbruch
- Optionaler Längenbegrenzer für Eingaben
- Audit-Hash zur Wiedererkennung
"""

import hashlib
import textwrap

MAX_USER_CHARS = 3000
MAX_DATA_CHARS = 5000

def sanitize_block(text: str) -> str:
    """
    Entfernt gefährliche Steuerzeichen und Prompt-Marker.
    """
    text = text.replace("###", "# # #")
    return text.strip()

def shorten(text: str, max_len: int) -> str:
    """
    Kürzt zu lange Texte auf max_len Zeichen.
    """
    if len(text) > max_len:
        return textwrap.shorten(text, width=max_len, placeholder="...[truncated]")
    return text

def build_prompt(system_prompt: str, user_prompt: str, clean_data: str = "") -> dict:
    """
    Erzeugt finalen Prompt. Rückgabe:
    {
        'prompt': str,
        'hash': str,
        'meta': dict
    }
    """

    # Sanitize + Kürzen
    system_block = sanitize_block(system_prompt)
    user_block = shorten(sanitize_block(user_prompt), MAX_USER_CHARS)
    data_block = shorten(sanitize_block(clean_data), MAX_DATA_CHARS) if clean_data else "[No external data provided]"

    prompt = f"""### SYSTEM ###
{system_block}

### USER ###
{user_block}

### DATA (filtered input) ###
{data_block}
"""

    # Hash für Audit-Zwecke
    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()

    print("[PromptBuilder] Finaler Prompt erzeugt.")
    return {
        "prompt": prompt,
        "hash": prompt_hash,
        "meta": {
            "user_len": len(user_block),
            "data_len": len(data_block),
            "truncated": len(user_prompt) > MAX_USER_CHARS or len(clean_data) > MAX_DATA_CHARS
        }
    }

"""
🚀 Vorteile

Feature	                            Effekt

🧱 Struktur-Schutz	                "###" wird entschärft → kein Fake-Systemblock
✂️ Textkürzung	                    Verhindert Overflow von Kontextlänge
🔐 SHA-256-Hash	                    Für Audit, Logging, oder Session-Wiederherstellung
📦 Rückgabe als Dict	            Macht Weiterverarbeitung sauber & strukturiert
📏 Meta-Daten	                    Zeigt, ob Inhalt gekürzt wurde

🔁 Integrationstipp
Im Agenten-Stack kann man damit z. B. nachvollziehen:

Welche Prompts zu welchen LLM-Antworten führten

Welche Session wie oft truncated == True getriggert hat (→ evtl. Split nötig)
"""

