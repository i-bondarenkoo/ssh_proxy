from fastapi import APIRouter, Body, Request
from app.schemas.proxy import ValidateDataIn

from typing import Annotated

router = APIRouter(
    tags=["Proxy"],
    # prefix='',
)


@router.post("/execute")
async def execute_command(
    request: Request,
    data_in: Annotated[
        ValidateDataIn, Body(description="IP unifi-точки и консольная команда")
    ],
):
    manager = request.app.state.ssh_manager
    response: dict = await manager.run(
        ip=data_in.ip,
        command=data_in.command.strip(),
    )
    return response
