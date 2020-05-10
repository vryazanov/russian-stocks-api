"""A set of functions to process query params."""


def to_bool(value: str) -> bool:
    """Transform raw value from query parameter to bool.

    >>> to_bool('True')
    True
    >>> to_bool('0')
    False
    """
    true_values = ('true', 't', '1')
    return value.strip().lower() in true_values
