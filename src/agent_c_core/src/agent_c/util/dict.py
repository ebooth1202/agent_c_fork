from typing import Any


def filter_dict_by_keys(source_dict, keys_to_include):
    """
    Create a new dictionary containing only the specified keys.

    :param source_dict: The original dictionary to filter.
    :param keys_to_include: An iterable of keys to include in the new dictionary.
    :return: A new dictionary with only the key-value pairs where the key is in keys_to_include.
    """
    return {key: source_dict[key] for key in keys_to_include if key in source_dict}

def set_nested(d: dict, path: str, value: Any, sep: str = "."):
    """Set a value in a nested dict given a path (dot or slash separated)."""
    keys = path.split(sep)
    current = d
    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value


def get_nested(d: dict, path: str, sep: str = ".") -> Any:
    """Get a value from a nested dict given a path, or None if missing."""
    keys = path.split(sep)
    current = d
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return None
        current = current[key]
    return current


def delete_nested(d: dict, path: str, sep: str = "."):
    """Delete a key from a nested dict if it exists."""
    keys = path.split(sep)
    current = d
    for key in keys[:-1]:
        if key not in current or not isinstance(current[key], dict):
            return
        current = current[key]
    current.pop(keys[-1], None)
