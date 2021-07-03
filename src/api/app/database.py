import os
import databases
import sqlalchemy

from fastapi import HTTPException
from fastapi.logger import logger

from .models import FilterProductsModel

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
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
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
database = databases.Database(DATABASE_URL)


async def filter_products(request_model: FilterProductsModel):
    query = Products.select()

    # simple filtering logic - just map the request fields to database model structure
    data_dict = request_model.dict()
    for column in Products.columns:
        filter_value = data_dict.get(column.name)
        if filter_value:
            query = query.where(column == filter_value)

    if request_model.start_year:
        query = query.where(Products.c.year >= request_model.start_year)

    if request_model.end_year:
        query = query.where(Products.c.year <= request_model.end_year)

    try:
        return await database.fetch_all(query)
    except Exception as ex:
        logger.error(ex)
        raise HTTPException(status_code=500, detail=f'Database error. {ex}')
