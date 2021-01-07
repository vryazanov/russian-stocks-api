"""DB connector and ORM models."""
import uuid

import sqlalchemy as sa
import sqlalchemy.ext.declarative
import sqlalchemy.dialects.postgresql


Base = sqlalchemy.ext.declarative.declarative_base()


class TickerModel(Base):
    """Ticker model."""

    __tablename__ = 'tickers'

    name = sa.Column(sa.Text, nullable=False)
    code = sa.Column(sa.Text, primary_key=True, unique=True, nullable=False)


class PaymentModel(Base):
    """Payment model."""

    __tablename__ = 'payments'

    id = sa.Column(
        sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True,
        default=uuid.uuid4, unique=True, nullable=False)
    ticker = sa.Column(sa.Text, nullable=False)
    date = sa.Column(sa.Date, nullable=False)
    amount = sa.Column(sa.Numeric(10, 2), nullable=False)
    is_forecast = sa.Column(sa.Boolean, nullable=False)
    source = sa.Column(sa.Text, nullable=False)
