from .enums.user_type import UserType
from .services.security import require_user_type
from .routers.roles_router import router as roles_router
from .routers.health_router import router as health_router
from .routers.organisation_router import router as organisations_router
from .routers.applications_router import router as applications_router
from .routers.contacts_router import router as contacts_router
from .routers.users_router import router as users_router
from .routers.onboarding_router import router as onboarding_router
from .routers.auth_router import router as auth_router
from .routers.employees_router import router as employees_router

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI

app = FastAPI()

app.include_router(
    roles_router,
    prefix="/roles",
    dependencies=[Depends(require_user_type(UserType.admin))],
)
app.include_router(health_router, prefix="/health")
app.include_router(organisations_router, prefix="/organisations")
app.include_router(applications_router, prefix="/applications")
app.include_router(contacts_router, prefix="/contacts")
app.include_router(users_router, prefix="/users")
app.include_router(employees_router, prefix="/users/employees")
app.include_router(onboarding_router, prefix="/onboarding")
app.include_router(auth_router, prefix="/auth")

origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # <-- only allow frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
