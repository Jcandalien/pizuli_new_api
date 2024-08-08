from fastapi import FastAPI,status
from services.tasks import update_franchise_status
from tortoise.contrib.fastapi import register_tortoise
from api.v1 import animal, auth, franchise, order, product, meat, recipe
from config import TORTOISE_ORM
from contextlib import asynccontextmanager
from fastapi import BackgroundTasks
import logging
from tortoise import Tortoise
from services.fileuploadmiddleware import FileUploadMiddleware
# from fastapiadmin.dashboard import setup_admin
from admin import setup_admin
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await Tortoise.init(config=TORTOISE_ORM)
        await Tortoise.generate_schemas(safe=True)
        yield
    except Exception as e:
        logging.error(f"An error occurred during startup: {str(e)}")
        raise
    finally:
        try:
            await Tortoise.close_connections()
        except Exception as e:
            logging.error(f"An error occurred during cleanup: {str(e)}")

app = FastAPI(
    title="PIZULI MEATS",
    description="API for managing the farm to plate supply chain",
    version="1.0.0",
    lifespan=lifespan,
    debug=True
)

@app.on_event("startup")
async def startup_event():
    background_tasks = BackgroundTasks()
    background_tasks.add_task(update_franchise_status)

app.add_middleware(FileUploadMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(franchise.router, prefix="/api/v1/franchises", tags=["Franchises"])
app.include_router(animal.router, prefix="/api/v1/animals", tags=["Animals"])
app.include_router(meat.router, prefix="/api/v1/meat", tags=["meats"])
app.include_router(order.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(recipe.router, prefix="/api/v1/recipes", tags=["recipes"])
app.include_router(product.router, prefix="/api/v1/products", tags=["Products"])

# Set up admin
admin_app = setup_admin()
app.mount("/admin", admin_app)

app.openapi_schema = None

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="PIZULI MEATS API",
        version="1.0.0",
        description="API for managing the farm to plate supply chain",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)},
    )

register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
