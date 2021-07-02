import uuid
from os import getenv
from fastapi import FastAPI, HTTPException

from .database import Products, database
from .models import FilterProductsModel, ResponseModel
from .s3 import upload_result

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/task", status_code=201)
async def create_task(data: FilterProductsModel):
    query = Products.select()

    # simple filtering logic - just map the request fields to database model structure
    data_dict = data.dict()
    for column in Products.columns:
        filter_value = data_dict.get(column.name)
        if filter_value:
            query = query.where(column == filter_value)

    if data.start_year:
        query = query.where(Products.c.year >= data.start_year)

    if data.end_year:
        query = query.where(Products.c.year <= data.end_year)

    products = await database.fetch_all(query)
    if products:
        result = list(map(dict, products))

        task_id = uuid.uuid4()
        upload_result(result, f'{task_id}/metadata.json')

        #TODO: Create celery task

        return {'task_id': task_id}
    else:
        raise HTTPException(status_code=404, detail="No items found for your request")
