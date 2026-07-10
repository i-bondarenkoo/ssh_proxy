from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from app.services.ssh_manager import SSHManager
from app.views.proxy import router as proxy_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ssh_manager = SSHManager()
    yield
    app.state.ssh_manager.close_all_ssh_sessions()


app = FastAPI(lifespan=lifespan)
app.include_router(proxy_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
