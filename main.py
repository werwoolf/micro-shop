from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from items_views import router as items_router
from users.views import router as users_router
from contextlib import asynccontextmanager
from core.models import Base, db_helper
from api_v1 import router as router_v1
from core.config import settings
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=router_v1, prefix=settings.api_vi_prefix)
app.include_router(items_router)
app.include_router(users_router)


@app.get("/", response_class=HTMLResponse)
async def root():
    return "<div>This is <b>bold</b> test</div>"

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=3456)
