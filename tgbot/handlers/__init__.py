"""Import all routers and add them to routers_list."""
from .admin import admin_router
from .user import user_router
from .quiz import quiz_router
from .training import train_router
routers_list = [
    admin_router,
    train_router,
    quiz_router,
    user_router,
]


__all__ = [
    "routers_list",
]
