from utils.midilogger import stamp

def parse_int(n):
    if isinstance(n, int):
        return n
    if isinstance(n, float):
        if n.is_integer():
            return int(n)
        else:
            stamp(2, f"Invalid value for integer: {n}")
            raise ValueError(f"Invalid value: {n}")
    if isinstance(n, str):
        n = n.strip()
        if n.isdigit() or (n.startswith('-') and n[1:].isdigit()):
            return int(n)
    stamp(2, f"Invalid value for integer: {n}")
    raise ValueError(f"Invalid value: {n}")

def parse_bool(n):
    if isinstance(n, bool):
        return n
    if isinstance(n, int):
        if n == 1:
            return True
        elif n == 0:
            return False
        else:
            stamp(2, f"Invalid value for boolean: {n}")
            raise ValueError(f"Invalid value: {n}")
    if isinstance(n, str):
        val = n.strip().lower()
        if val in ['true', '1']:
            return True
        elif val in ['false', '0']:
            return False
    stamp(2, f"Invalid value for boolean: {n}")
    raise ValueError(f"Invalid value: {n}")