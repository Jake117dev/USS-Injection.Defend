"""
cache_manager.py

Verwaltet flüchtige Prompt-Daten im RAM.
- Unterstützt SHA256-basiertes Caching
- Optionaler Ablaufzeitpunkt (TTL)
- Ideal für Replay, Audit oder temporäre Session-Haltung
"""

import time
import hashlib
from typing import Dict, Optional

class CacheEntry:
    def __init__(self, prompt: str, ttl: int = 300):
        self.prompt = prompt
        self.created_at = time.time()
        self.ttl = ttl  # Time to live in seconds

    def is_expired(self) -> bool:
        return (time.time() - self.created_at) > self.ttl

    def age(self) -> float:
        return time.time() - self.created_at


class PromptCache:
    def __init__(self):
        self._cache: Dict[str, CacheEntry] = {}

    def _generate_hash(self, prompt: str) -> str:
        return hashlib.sha256(prompt.encode("utf-8")).hexdigest()

    def store(self, prompt: str, ttl: int = 300) -> str:
        key = self._generate_hash(prompt)
        self._cache[key] = CacheEntry(prompt, ttl)
        print(f"[CacheManager] Prompt gespeichert: {key}")
        return key

    def retrieve(self, key: str) -> Optional[str]:
        entry = self._cache.get(key)
        if entry and not entry.is_expired():
            print(f"[CacheManager] Prompt gefunden: {key}")
            return entry.prompt
        elif entry:
            print(f"[CacheManager] Prompt abgelaufen: {key}")
            self._cache.pop(key, None)
        return None

    def exists(self, key: str) -> bool:
        return key in self._cache and not self._cache[key].is_expired()

    def cleanup(self):
        expired_keys = [k for k, v in self._cache.items() if v.is_expired()]
        for k in expired_keys:
            del self._cache[k]
        print(f"[CacheManager] {len(expired_keys)} Einträge entfernt (abgelaufen).")

    def stats(self) -> dict:
        return {
            "entries": len(self._cache),
            "active": sum(1 for e in self._cache.values() if not e.is_expired()),
            "expired": sum(1 for e in self._cache.values() if e.is_expired())
        }

"""
 🧠 Features im Überblick
 
Funktion	            Wirkung

🧠 In-Memory	        Kein Disk- oder Netzwerk-Overhead – läuft super leicht auf Pi & Tower
🔐 SHA256 Hash	        Nutzt prompt content als Fingerabdruck für Cache-Key
⏳ TTL Support	        Jeder Prompt kann automatisch nach X Sekunden verfallen
🔁 Replay-fähig	        Man kann exakt denselben Prompt wieder abrufen (z. B. für Audits)
🧹 Cleanup-Modus	    Entfernt automatisch veraltete Einträge → keine RAM-Leaks


💾 Warum ein cache_manager.py Sinn macht
1. Schnelle Wiederverwendung von Prompts
Man baut dynamische Prompts – aber:

User-Eingaben können sich ähneln

System- oder Datenkontexte wiederholen sich
→ Caching spart dir LLM-Ressourcen & Verarbeitungszeit

⏭️ So könnte man es nutzen:

from cache_manager import PromptCache

cache = PromptCache()
hash_key = cache.store(prompt_text, ttl=600)

 später…
prompt_reloaded = cache.retrieve(hash_key)

 periodisch aufräumen
cache.cleanup()

2. RAM-isolierter Zwischenspeicher = Teil deiner Sicherheitsarchitektur:
„RAM/Cache – flüchtige Kontexte werden isoliert, bei Bedarf referenziert“

Das bedeutet:
Kein dauerhafter Speicher (datenschutzfreundlich)
Aber temporäre Referenzierbarkeit über Session-Tokens, URL, etc.

3. Audit & Replay-fähig
Mit dem SHA-256-Hash aus prompt_builder.py kann man:

Prompt-Versionen loggen
später genau denselben Prompt rekonstruieren
feststellen, ob Angreifer etwas „verändert“ haben

4. Modular ausbaubar
Kann später:
Memory-TTL einbauen (nach X Minuten wird gelöscht)

Token-Limiter (max. Y Prompts pro Session)
"""

#In-Memory + optional File/Redis speichern

