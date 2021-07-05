import os
from celery import Celery, states
from fastapi import FastAPI, HTTPException

from app.models import FilterProductsModel
from app.celery import tasks

app = FastAPI()
tasks = Celery(broker=os.getenv('BROKER_URL'), backend=os.getenv('REDIS_URL'))


@app.post("/task", status_code=201)
async def create_task(data: FilterProductsModel):
    try:
        task = tasks.send_task(
            name='products.filter',
            kwargs=data.dict(),
            queue='products'
        )

        return {'task_id': task.id}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Cannot process the task: {ex}")
