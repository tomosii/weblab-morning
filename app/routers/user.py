from fastapi import APIRouter, Request, Response

router = APIRouter()


@router.post("/checkin")
async def checkin():
    return {"message": "checkin"}
