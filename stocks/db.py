"""DB connector and ORM models."""
import datetime
import uuid

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql
import sqlalchemy.ext.declarative


Base = sqlalchemy.ext.declarative.declarative_base()


class TokenModel(Base):
    """Token model."""

    __tablename__ = 'tokens'

    token = sa.Column(sa.Text, primary_key=True, unique=True, nullable=False)


class TickerModel(Base):
    """Ticker model."""

    __tablename__ = 'tickers'

    name = sa.Column(sa.Text, nullable=False)
    code = sa.Column(sa.Text, primary_key=True, unique=True, nullable=False)
    log = sa.Column(sa.Integer)


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


class QuoteModel(Base):
    """Quote model."""

    __tablename__ = 'quotes'

    id = sa.Column(
        sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True,
        default=uuid.uuid4, unique=True, nullable=False)
    ticker = sa.Column(sa.Text, nullable=False)
    date = sa.Column(sa.Date, nullable=False)
    open_price = sa.Column(sa.Numeric(10, 2), nullable=False)
    close_price = sa.Column(sa.Numeric(10, 2), nullable=False)


class PfOperationModel(Base):
    """Portfolio operation."""

    __tablename__ = 'pf_operations'

    id = sa.Column(
        sqlalchemy.dialects.postgresql.UUID(as_uuid=True), primary_key=True,
        default=uuid.uuid4, unique=True, nullable=False)

    ticker = sa.Column(sa.Text, sa.ForeignKey('tickers.code'), nullable=False)
    token = sa.Column(sa.Text, sa.ForeignKey('tokens.token'), nullable=False)
    action = sa.Column(sa.Text, nullable=False)
    quantity = sa.Column(sa.Integer, nullable=False)
    price = sa.Column(sa.Numeric(10, 2), nullable=False)
    performed_at = sa.Column(sa.DateTime, default=datetime.datetime.utcnow)
