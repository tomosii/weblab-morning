def get_point_change(time_difference_seconds: float):
    diff_hour = int(time_difference_seconds // 3600)
    if diff_hour > 0:
        points = -min(diff_hour, 3)
    else:
        points = 1
    print(f"Points: {points}")
