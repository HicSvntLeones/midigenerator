import importlib


__all__ = ["logger"]

def __getattr__(name):
    if name == "logger":
        from .hsl_logger.hsl_logger import HSLLogger
        instance = HSLLogger()
        globals()[name] = instance  # Cache it for future imports
        return instance
    


    raise AttributeError(f"module {__name__} has no attribute {name}")

