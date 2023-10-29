from app.models.attendance import Attendance


def get_point_change(time_difference_seconds: float):
    if time_difference_seconds < 0:
        return 1

    late_hour = time_difference_seconds / 3600
    print(f"Late hour: {late_hour:.1f}")
    penalty = int(late_hour // 2 + 1)
    return -min(penalty, 3)


def get_total_points_and_penalty(user_id: str, attendances: list[Attendance]):
    total_points = 0
    penalty = 0
    for attendance in attendances:
        if attendance.user_id != user_id:
            continue
        point_change = get_point_change(attendance.time_difference_seconds)
        print(f"{attendance.date} {point_change}")
        total_points += point_change
        if point_change < 0:
            penalty += point_change

    return total_points, penalty
