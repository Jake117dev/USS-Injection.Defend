# prompt_builder.py
"""
Erzeugt den finalen Prompt-Kontext aus:
- system_prompt (fest)
- user_prompt (original oder bereinigt)
- optionaler Dateninput (z. B. aus Webseite oder PDF)
"""

def build_prompt(system_prompt: str, user_prompt: str, clean_data: str = "") -> str:
    """
    Baut den finalen Prompt in strukturierter Form.
    """

    prompt = f"""### SYSTEM ###
{system_prompt.strip()}

### USER ###
{user_prompt.strip()}

### DATA (filtered input) ###
{clean_data.strip() if clean_data else '[No external data provided]'}
"""

    print("[PromptBuilder] Finaler Prompt erzeugt.")
    return prompt
