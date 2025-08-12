import time

log_level = 1
include_time = False

def stamp(level = 5, msg=""):
    if level > log_level:
        return
    level_str = "[VERBOSE]"
    match level:
        case 1:
            level_str = "[CRITICAL]"
        case 2:
            level_str = "[WARNING]"
        case 3:
            level_str = "[DEBUG]"
        case 4:
            level_str = "[TRACE]"
        case _:
            pass

    if include_time:
        current_time = time.strftime('%H:%M:%S')
    else:
        current_time = ''
    print(f"{level_str} {current_time} - {msg}")

def set_log_level(n):
    global log_level 
    log_level = n
    stamp(4, f"Log level set to {n}")

def set_log_time(n):
    global include_time
    include_time = n
    stamp(4, f"Include debug timestamps set to {n}")