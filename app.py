import os
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi.responses import UJSONResponse
from fastapi import Request
from fastapi import FastAPI
from database.connection import create_pg_pool
from service.utils import build_get_marker_builder
from views.handle_map_markers import handle_get_map_markers
import uvicorn

app = FastAPI(
    title='Map MicroService',
    description='Map MicroService For Mpeix',
    default_response_class=UJSONResponse

)


@app.middleware('http')
async def add_connection(req: Request, call_next):
    conn = await pool.acquire()
    req.scope['pg_connection'] = conn
    response = await call_next(req)
    await pool.release(conn)
    return response


@app.exception_handler(500)
async def handle_exception(req: Request, exc: Exception):
    return {
        'data': None,
        'error': str(exc)
    }


@app.on_event('startup')
async def on_startup():
    global pool
    dsn = os.getenv('DB_URL')
    port = os.getenv('PORT')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    pool = await create_pg_pool(dsn, password, user)
    FastAPICache.init(InMemoryBackend())


@app.get('/v1/marker/')
@cache(expire=60, key_builder=build_get_marker_builder)
async def get_map_markers(req: Request):
    print('not-cached')
    conn = req.scope['pg_connection']
    data = await handle_get_map_markers(conn)
    return {
        'markers': data
    }