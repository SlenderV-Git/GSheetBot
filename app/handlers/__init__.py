from aiogram import Router
from app.middlewares.base_middlewares import BaseMiddleware
from .admin import rt as admin_rt

def get_root_rt():
    rt = Router()
    rt.include_router(admin_rt)
    rt.message.middleware.register(BaseMiddleware())
    
    return rt