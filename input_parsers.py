from midilogger import stamp

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