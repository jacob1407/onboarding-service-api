from .routers.roles_router import router as roles_router
from .routers.health_router import router as health_router
from .routers.organisation_router import router as organisations_router
from .routers.applications_router import router as applications_router
from .routers.contacts_router import router as contacts_router
from .routers.users_router import router as users_router
from .routers.onboarding_router import router as onboarding_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

app = FastAPI()

app.include_router(roles_router, prefix="/roles")
app.include_router(health_router, prefix="/health")
app.include_router(organisations_router, prefix="/organisations")
app.include_router(applications_router, prefix="/applications")
app.include_router(contacts_router, prefix="/contacts")
app.include_router(users_router, prefix="/users")
app.include_router(onboarding_router, prefix="/onboarding")

origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # <-- only allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
