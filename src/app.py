from .routers.employees_router import router as employees_router
from .routers.roles_router import app as roles_router
from .routers.health_router import app as health_router
from .routers.organisation_router import app as organisations_router
from .routers.templates_router import app as templates_router

from fastapi import FastAPI

app = FastAPI()

app.include_router(employees_router, prefix="/employees")
app.include_router(roles_router, prefix="/roles")
app.include_router(health_router, prefix="/health")
app.include_router(organisations_router, prefix="/organisations")
app.include_router(templates_router, prefix="/templates")
