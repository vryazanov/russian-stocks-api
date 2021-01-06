"""High-level entities."""
import datetime
import decimal
import enum

import pydantic


class Source(str, enum.Enum):
    """Source of data."""

    dohod = 'dohod'
    smartlab = 'smartlab'


class Ticker(pydantic.BaseModel):
    """Ticker."""

    name: str
    code: str

    def to_mongo(self) -> dict:
        """Convert to mongo structure."""
        return {
            'name': self.name,
            'code': self.code,
        }


class Payment(pydantic.BaseModel):
    """Dividends payment."""

    ticker: str
    date: datetime.date
    open_price: decimal.Decimal
    close_price: decimal.Decimal
    is_forecast: bool
    source: Source

    def to_mongo(self) -> dict:
        """Convert to mongo structure."""
        return {
            'ticker': self.ticker,
            'date': datetime.datetime.combine(self.date, datetime.time.min),
            'open_price': str(self.open_price),
            'close_price': str(self.close_price),
            'is_forecast': self.is_forecast,
            'source': str(self.source),
        }
