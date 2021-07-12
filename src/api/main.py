import os

from celery import Celery, signature, states
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

from app.models import FilterProductsModel, TaskResult

app = FastAPI()
tasks = Celery(broker=os.getenv('BROKER_URL'), backend=os.getenv('REDIS_URL'))


@app.post("/task", status_code=201)
async def create_task(data: FilterProductsModel):
    try:
        task = signature('filter', kwargs=data.dict(), queue='imagery')

        if data.apply_model:
            task = task | signature('model', queue='inference')

        task_details = task.apply_async()

        return {'task_id': task_details.id}
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Cannot process the task: {ex}")


@app.get("/task/{task_id}", status_code=200)
def get_task_result(task_id: str):
    result = tasks.AsyncResult(task_id)

    output = TaskResult(
        id=task_id,
        status=result.state,
        error=str(result.info) if result.failed() else None,
        result=result.get() if result.state == states.SUCCESS else None
    )

    return JSONResponse(
        content=output.dict()
    )
