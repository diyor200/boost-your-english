"""Import all routers and add them to routers_list."""
from .admin import admin_router
from .user import user_router
from .contest import contest_router
from .subject import subject_router
routers_list = [
    admin_router,
    subject_router,
    contest_router,
    user_router,
]


__all__ = [
    "routers_list",
]
