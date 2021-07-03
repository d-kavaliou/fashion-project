import uuid
from fastapi import FastAPI, HTTPException

from app.database import filter_products, database
from app.models import FilterProductsModel
from app.s3 import upload_result
from app.celery import tasks

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/task", status_code=201)
async def create_task(data: FilterProductsModel):
    products = await filter_products(data)

    if products:
        result = list(map(dict, products))

        result_id = uuid.uuid4()
        s3_target = await upload_result(result, f'{result_id}/metadata.json')

        task = tasks.send_task(
            name='products.filter',
            kwargs=data.dict(),
            queue='products'
        )

        return {'task_id': task.id}
    else:
        raise HTTPException(status_code=404, detail="No items found for your request")
