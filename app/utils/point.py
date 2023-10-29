from app.models.attendance import Attendance


def get_point_change(time_difference_seconds: float):
    diff_hour = int(time_difference_seconds // 3600)
    if diff_hour > 0:
        points = -min(diff_hour, 3)
    else:
        points = 1
    return points


def get_total_points_and_penalty(user_id: str, attendances: list[Attendance]):
    total_points = 0
    penalty = 0
    for attendance in attendances:
        if attendance.user_id != user_id:
            continue
        point_change = get_point_change(attendance.time_difference_seconds)
        total_points += point_change
        if point_change < 0:
            penalty += point_change

    return total_points, penalty
