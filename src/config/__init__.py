try:
    from .config import HELL_CONFIG as HELL_CONFIG
except ImportError as _:
    from .example_config import HELL_CONFIG as HELL_CONFIG
