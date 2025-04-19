from .routers.employees_router import router as employees_router
from .routers.roles_router import router as roles_router
from .routers.health_router import router as health_router
from .routers.organisation_router import router as organisations_router
from .routers.templates_router import router as templates_router
from .routers.applications_router import router as applications_router
from .routers.contacts_router import router as contacts_router

from fastapi import FastAPI

app = FastAPI()

app.include_router(employees_router, prefix="/employees")
app.include_router(roles_router, prefix="/roles")
app.include_router(health_router, prefix="/health")
app.include_router(organisations_router, prefix="/organisations")
app.include_router(templates_router, prefix="/templates")
app.include_router(applications_router, prefix="/applications")
app.include_router(contacts_router, prefix="/contacts")
