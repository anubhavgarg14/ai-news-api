import json
from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from starlette.responses import Response


router = APIRouter()

security = HTTPBearer()
API_TOKEN = "your-secret-token"


class EventSchema(BaseModel):
    """Event Schema"""

    event_id: str
    event_type: str
    event_data: dict


"""
Becuase of the router, every endpoint in this file is prefixed with /events/
"""


@router.post("/")
def handle_event(
    data: EventSchema,
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Response:
    if credentials.credentials != API_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
        )

    print(data)

    # Return acceptance response
    return Response(
        content=json.dumps({"message": "Data received!"}),
        status_code=HTTPStatus.ACCEPTED,
    )
