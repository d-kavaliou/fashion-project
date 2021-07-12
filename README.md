Fashion project
====================
A PoC project for fashion industry - made to be extensible and stable.

## Installation
Please, prepare the data: [Fashion Dataset](https://www.kaggle.com/paramaggarwal/fashion-product-images-small). Download the archive and extract it to `DATASET_PATH` from Makefile (or specify your own path).
```sh
make build
# make test - !tests are not implemented for now
```
## Run
```sh
make up
```
## Finish
```sh
make down
```
After running the command, there will be printed url to Jupyter notebook mapped to your localhost port.
## Architecture
![Architecture](./docs/diagrams/architecture.png)
## Components
### API
[FastAPI](https://fastapi.tiangolo.com/) framework was chosen due to its performance and intuitiveness.
It provides a bunch of useful bultin features: asyncio support, data validation and documentation generation:
![Documentation](./docs/images/swagger.png)

Also, according to [Benchmarks](https://www.techempower.com/benchmarks/#section=test&runid=7464e520-0dc2-473d-bd34-dbdfd7e85911&hw=ph&test=query&l=zijzen-7)
its SOTA web framework for Python ecosystem.

The main responsibilities of the component: 
- user authentication
- data validation 
- tasks registration
- status checking.

After validation of the request it sends task to `imagery` workers. And in case of `apply_model=True` it also chains `inference` after the original task. 

> In terms of performance, we can consider to use LoadBalancer for this part of the application if we encounter a huge requests load.
### Celery message broker and backend
