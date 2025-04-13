from .routers.users_router import app as users_router
from .routers.roles_router import app as roles_router
from .routers.health import app as health_router
from .db import Base, engine

from fastapi import FastAPI

app = FastAPI()

app.include_router(users_router, prefix="/users")
app.include_router(roles_router, prefix="/roles")
app.include_router(health_router, prefix="/health")
