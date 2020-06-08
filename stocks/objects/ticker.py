"""Objects to work with ticker."""


class Ticker:
    """Stock ticker."""

    def __init__(self, code: str):
        """Primary constructor."""
        self._code = code
