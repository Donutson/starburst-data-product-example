"""
Str functions
"""
import re


def is_upper_camel_case(name: str, sep_char=" "):
    for word in name.split(sep_char):
        if not word[0].isupper() and not word[1:].islower():
            return False
    return True


def to_snake_case(name):
    """
    Convert a string to snake_case.

    Args:
        s (str): The input string to be converted.

    Returns:
        str: The converted snake_case string.
    """
    # Replace spaces, hyphens, and periods with underscores
    name = re.sub(r"[\s\-\.\,]+", "_", name)

    # Insert underscores before capital letters (handling camelCase and PascalCase)
    name = re.sub(r"(?<!^)(?=[A-Z])", "_", name)

    # Convert the string to lowercase
    name = name.lower()

    # Remove any leading or trailing underscores
    name = name.strip("_")

    return name


def is_snake_case(s: str) -> bool:
    """
    Checks if the given string is in snake_case format with numbers allowed but not at the beginning.

    Args:
    s (str): The string to check.

    Returns:
    bool: True if the string is in snake_case with numbers allowed but not at the beginning, False otherwise.
    """
    # Pattern for snake_case with numbers allowed but not at the beginning
    pattern = re.compile(r"^[a-z]+(_[a-z0-9]+)*$")
    return bool(pattern.match(s))
