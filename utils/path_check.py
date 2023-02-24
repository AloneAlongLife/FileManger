from os.path import abspath, commonpath, samefile
from config import ALLOW_PATH


def check(path: str) -> bool:
    try:
        path = abspath(path)
        allow_commons = tuple(filter(lambda a_path: samefile(
            commonpath((path, a_path)), a_path), ALLOW_PATH.allow))
        if len(allow_commons) == 0:
            return False
        exclude_commons = tuple(filter(lambda e_path: samefile(
            commonpath((path, e_path)), e_path), ALLOW_PATH.exclude))
        if len(exclude_commons) != 0:
            return False
        return True
    except Exception:
        return None
    
