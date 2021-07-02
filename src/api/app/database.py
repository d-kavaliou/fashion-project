import os
import databases
import sqlalchemy

host = os.environ["POSTGRES_HOST"]
port = os.environ["POSTGRES_PORT"]
user = os.environ["POSTGRES_USER"]
password = os.environ["POSTGRES_PASS"]
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
