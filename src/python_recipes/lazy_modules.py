"""
Lazy module loading.

Use this module as:

```python
from python_recipes import lazy_modules
```

Modules are imported on first access:

```python
lazy_modules.json.loads()
lazy_modules.sys.version
```

Always access modules through this pattern to ensure deferred loading.

For type-checking support, declare modules under `TYPE_CHECKING`.
Use `# noqa: F401` to prevent linters from removing the imports:

```python
if TYPE_CHECKING:
    import json  # noqa: F401
    import sys  # noqa: F401
```

"""

import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import json

    import requests

__all__ = [
    "json",
    "requests",
    "sys",
]


def __getattr__(name: str) -> object:
    if name == "__path__":
        raise AttributeError(name)
    if name not in sys.modules:
        from importlib import import_module

        sys.modules[name] = import_module(name)
    return sys.modules[name]
