import os
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from fastapi.responses import UJSONResponse
from fastapi import Request
from fastapi import FastAPI
from database.connection import create_pg_pool
from views.handle_map_markers import handle_get_map_markers

app = FastAPI(
    title='Map MicroService',
    description='Map MicroService For Mpeix',
    default_response_class=UJSONResponse

)


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
@cache(expire=60)
async def get_map_markers():
    conn = await pool.acquire()
    data = await handle_get_map_markers(conn)
    await pool.release(conn)
    return {
        'markers': data
    }