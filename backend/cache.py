"""Tiny bounded cache; replace with RedisCache in a multi-instance deployment."""
from __future__ import annotations

import hashlib
import json
from collections import OrderedDict
from typing import Any


class SemanticLRUCache:
    def __init__(self, max_size: int = 128) -> None:
        self.max_size = max_size
        self._items: OrderedDict[str, Any] = OrderedDict()

    @staticmethod
    def key(prompt: str) -> str:
        normalized = " ".join(prompt.lower().split())
        return hashlib.sha256(normalized.encode()).hexdigest()

    def get(self, prompt: str) -> Any | None:
        key = self.key(prompt)
        value = self._items.get(key)
        if value is not None:
            self._items.move_to_end(key)
        return value

    def set(self, prompt: str, value: Any) -> None:
        key = self.key(prompt)
        self._items[key] = value
        self._items.move_to_end(key)
        if len(self._items) > self.max_size:
            self._items.popitem(last=False)


cache = SemanticLRUCache()
