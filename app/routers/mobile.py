import datetime

from fastapi import APIRouter, HTTPException, Security
from pydantic import BaseModel
from geopy.distance import geodesic
from zoneinfo import ZoneInfo
from app.repository.firebase import (
    place_repository,
    user_repository,
    attendance_repository,
    commitment_repository,
    point_repository,
)
from app.auth.api_key import api_key_auth
from app.views import checkin_notification
from app.repository.slack import slack_repository
from app.constants import TARGET_CHANNEL_ID
from app.utils import weekday, point, time_difference

router = APIRouter()

slack_client = slack_repository.client


class CheckInRequest(BaseModel):
    email: str
    latitude: float
    longitude: float
    ip_address: str


@router.post("/checkin", dependencies=[Security(api_key_auth)])
async def checkin(checkin_request: CheckInRequest):
    print(f"Received checkin request from {checkin_request.email}")
    print(checkin_request)

    checkin_at = datetime.datetime.now(ZoneInfo("Asia/Tokyo"))
    print("Current time: ", checkin_at)

    user = user_repository.get_user(checkin_request.email)
    if user is None:
        print(f"User not found: {checkin_request.email}")
        raise HTTPException(
            status_code=400,
            detail="User not found.",
        )

    places = place_repository.get_places()

    checkin_place = None
    for place in places:
        for place_ip in place.ip_addresses:
            if place_ip in checkin_request.ip_address:
                print(f"IP address matched with {place.name}.")
                checkin_place = place
                break

    if checkin_place is None:
        print("IP address not matched with any place.")
        raise HTTPException(
            status_code=400,
            detail="IP address not matched with any place.",
        )

    distaces = geodesic(
        (checkin_request.latitude, checkin_request.longitude),
        (checkin_place.lat_lng.latitude, checkin_place.lat_lng.longitude),
    ).meters

    print(f"Distance: {distaces}")
    if distaces > 30:
        print("Distance is too far.")
        raise HTTPException(
            status_code=400,
            detail="Out of range of the check-in area.",
        )

    # Get today's commitments
    commits = commitment_repository.get_commit(
        date=checkin_at.date(),
    )

    # Check if the user has committed today
    for commit in commits:
        if commit.user_id == user.id:
            user_commit = commit
            break
    else:
        print("User has not committed today.")
        raise HTTPException(
            status_code=400,
            detail="User doesn't have a commitment today.",
        )

    commit_datetime = datetime.datetime.replace(
        checkin_at,
        hour=int(user_commit.time.split(":")[0]),
        minute=int(user_commit.time.split(":")[1]),
        second=0,
        microsecond=0,
    )
    print(f"Commitment time: {user_commit.time}")
    print("Commitment datetime: ", commit_datetime)

    # Check if the user has already checked in today
    attendances = attendance_repository.get_attendance(
        date=checkin_at.date(),
    )
    for attendance in attendances:
        if attendance.user_id == user.id:
            print("User has already checked in today.")
            raise HTTPException(
                status_code=400,
                detail="Already checked in today.",
            )
    else:
        print("User has not checked in yet today.")

    time_diff_seconds = time_difference.get_time_difference_seconds(
        commit_time=user_commit.time,
        checkin_at=checkin_at,
    )
    print(f"Time difference: {time_diff_seconds} seconds")
    today_point_change = point.get_point_change(time_diff_seconds)
    print(f"Point change: {today_point_change}")

    attendance_repository.put_attendance(
        user_id=user.id,
        user_name=user.nickname,
        checkin_at=checkin_at,
        commitment_time=user_commit.time,
        ip_address=checkin_request.ip_address,
        latitude=checkin_request.latitude,
        longitude=checkin_request.longitude,
        place_name=checkin_place.name,
        time_difference_seconds=time_diff_seconds,
    )

    # Calculate total points this week from attendance
    ongoing_activity_dates = weekday.get_ongoing_or_last_weekdays()
    attendances = attendance_repository.get_attendances(
        dates=ongoing_activity_dates,
    )

    tota_points, penalty = point.get_total_points_and_penalty(
        user_id=user.id,
        attendances=attendances,
    )

    print(f"Total points: {tota_points}")
    print(f"Total penalty: {penalty}")

    slack_client.chat_postMessage(
        channel=TARGET_CHANNEL_ID,
        blocks=checkin_notification.blocks(
            user_id=user.id,
            place_name=checkin_place.name,
            checkin_at=checkin_at,
            time_difference_seconds=time_diff_seconds,
            total_points=tota_points,
            point_change=today_point_change,
        ),
        text=checkin_notification.text(
            user_id=user.id,
        ),
    )
    print("Sent checkin notification.")

    # Update user's point
    point_repository.put_point(
        start_date=ongoing_activity_dates[0],
        user_id=user.id,
        user_name=user.nickname,
        point=tota_points,
        penalty=penalty,
    )

    return {
        "place_id": checkin_place.id,
        "place_name": checkin_place.name,
        "time_difference_seconds": time_diff_seconds,
    }
