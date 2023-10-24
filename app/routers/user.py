from fastapi import APIRouter, Request, Response, HTTPException
from pydantic import BaseModel
from geopy.distance import geodesic

from app.repository.firebase import place_repository

router = APIRouter()


class CheckInRequest(BaseModel):
    email: str
    latitude: float
    longitude: float
    ip_address: str


@router.post("/checkin")
async def checkin(checkin_request: CheckInRequest):
    print(f"Received checkin request from {checkin_request.email}")
    print(checkin_request)

    places = place_repository.get_places()
    print(places)

    checkin_place = None
    for place in places:
        for ip_address in place.ip_addresses:
            if checkin_request.ip_address in ip_address:
                print(f"IP address matched with {place.name}")
                checkin_place = place
                break

    if checkin_place is None:
        print("IP address not matched with any place.")
        return HTTPException(
            status_code=400,
            detail="IP address not matched with any place.",
        )

    distaces = geodesic(
        (checkin_request.latitude, checkin_request.longitude),
        (checkin_place.lat_lng.latitude, checkin_place.lat_lng.longitude),
    ).meters

    print(f"Distance: {distaces}")
    if distaces > 40:
        print("Distance is too far.")
        return HTTPException(
            status_code=400,
            detail="User is too far from the place.",
        )

    return {"message": "checkin"}
