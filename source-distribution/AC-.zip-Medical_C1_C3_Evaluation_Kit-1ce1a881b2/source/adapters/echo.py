"""Echo adapter for dry runs (no network)."""
from typing import List, Dict

class EchoAdapter:
    def __init__(self, **kwargs):
        pass

    def chat(self, messages: List[Dict[str,str]]) -> str:
        last = ''
        for m in messages[::-1]:
            if m.get('role') == 'user':
                last = m.get('content','')
                break
        return '[ECHO]\n' + last[:2000]
