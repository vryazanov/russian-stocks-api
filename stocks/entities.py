"""High-level entities."""
import datetime
import decimal
import enum
import secrets
import typing
import uuid

import pydantic


TokenCode = typing.NewType('TokenCode', str)
TickerCode = typing.NewType('TickerCode', str)


class Source(str, enum.Enum):
    """Source of data."""

    dohod = 'dohod'
    smartlab = 'smartlab'


class Ticker(pydantic.BaseModel):
    """Ticker."""

    name: str
    code: TickerCode
    lot: typing.Optional[int]

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


class Token(pydantic.BaseModel):
    """Token."""

    token: TokenCode

    class Config:
        """Model config."""

        orm_mode = True

    @classmethod
    def generate(cls) -> 'Token':
        """Generate random token."""
        return Token(token=secrets.token_hex(nbytes=16))


class PfAction(str, enum.Enum):
    """Portfolio action."""

    sell = 'sell'
    buy = 'buy'


class PfOperationBase(pydantic.BaseModel):
    """Base portfolio operation."""

    action: PfAction

    ticker: str
    quantity: int
    price: decimal.Decimal  # per one

    class Config:
        """Model config."""

        orm_mode = True


class PfOperationCreate(PfOperationBase):
    """Entity to create operation."""

    token: TokenCode


class PfOperation(PfOperationBase):
    """Portfolio operation."""

    id: uuid.UUID
    performed_at: datetime.datetime


class PfPosition(pydantic.BaseModel):
    """Portfolio position."""

    ticker: TickerCode
    quantity: int

    class Config:
        """Model config."""

        orm_mode = True


class PfSummary(pydantic.BaseModel):
    """Portfolio summary."""

    positions: typing.List[PfPosition]

    class Config:
        """Model config."""

        orm_mode = True
