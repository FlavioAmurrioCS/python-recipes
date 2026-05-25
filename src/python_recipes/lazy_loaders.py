from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Any

    import requests


class LazyLoader:
    @cached_property
    def json_loads(self) -> Callable[[str | bytes | bytearray], Any]:
        loads: Callable[[str | bytes | bytearray], Any]
        try:
            from orjson import loads

        except ImportError:
            from json import loads

        return loads

    @cached_property
    def json_dumps(self) -> Callable[[Any], str]:
        try:
            from orjson import dumps as orjson_dumps

            return lambda obj: orjson_dumps(obj).decode()
        except ImportError:
            from json import dumps as json_dumps

            return json_dumps

    @cached_property
    def requests_session(self) -> requests.Session:
        import requests

        return requests.Session()


lazy = LazyLoader()
