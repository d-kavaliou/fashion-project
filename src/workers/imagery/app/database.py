import os
import sqlalchemy

from sqlalchemy import create_engine
from celery.utils.log import get_logger

logger = get_logger(__name__)

host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASSWORD"]
db = os.environ["POSTGRES_DB"]

DATABASE_URL = f"postgresql://{user}:{password }@{host}:{port}/{db}"

metadata = sqlalchemy.MetaData()
Products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("image_id", sqlalchemy.String),
    sqlalchemy.Column("gender", sqlalchemy.String),
    sqlalchemy.Column("master_category", sqlalchemy.String),
    sqlalchemy.Column("sub_category", sqlalchemy.String),
    sqlalchemy.Column("article_type", sqlalchemy.String),
    sqlalchemy.Column("base_colour", sqlalchemy.String),
    sqlalchemy.Column("season", sqlalchemy.String),
    sqlalchemy.Column("year", sqlalchemy.Integer),
    sqlalchemy.Column("usage", sqlalchemy.String),
    sqlalchemy.Column("display_name", sqlalchemy.String)
)
engine = create_engine(DATABASE_URL)


def filter_products(data_dict: dict):
    query = Products.select()

    # simple filtering logic - just map the request fields to database model structure
    for column in Products.columns:
        filter_value = data_dict.get(column.name)
        if filter_value:
            query = query.where(column == filter_value)

    start_year, end_year = data_dict.get('start_year'), data_dict.get('end_year')
    if start_year:
        query = query.where(Products.c.year >= start_year)

    if end_year:
        query = query.where(Products.c.year <= end_year)

    try:
        with engine.connect() as conn:
            result = conn.execute(query).fetchall()
            logger.info(f'{len(result)} rows have been selected.')

            return result
    except Exception as ex:
        logger.error(ex)
        raise Exception(f'Database interaction error: {ex}')
