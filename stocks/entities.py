"""High-level entities."""
import datetime
import decimal
import enum
import typing
import uuid

import pydantic


TickerCode = typing.NewType('TickerCode', str)


class Source(str, enum.Enum):
    """Source of data."""

    dohod = 'dohod'
    smartlab = 'smartlab'


class Ticker(pydantic.BaseModel):
    """Ticker."""

    name: str
    code: TickerCode

    class Config:
        """Model config."""

        orm_mode = True


class QuoteBase(pydantic.BaseModel):
    """Base stock quote."""

    ticker: TickerCode
    date: datetime.date
    open_price: decimal.Decimal
    close_price: decimal.Decimal

    class Config:
        """Model config."""

        orm_mode = True


class Quote(QuoteBase):
    """Quote entity."""

    id: uuid.UUID


class QuoteCreate(QuoteBase):
    """Entity to create quote."""


class PaymentBase(pydantic.BaseModel):
    """Base dividend payment."""

    ticker: TickerCode
    date: datetime.date
    amount: decimal.Decimal
    is_forecast: bool
    source: Source

    class Config:
        """Model config."""

        orm_mode = True


class Payment(PaymentBase):
    """Payment entity."""

    id: uuid.UUID


class PaymentCreate(PaymentBase):
    """Entity to create payment."""
