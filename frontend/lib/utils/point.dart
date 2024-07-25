int getPointChange(double timeDifferenceSeconds) {
  if (timeDifferenceSeconds < 0) {
    return 1;
  }
  final lateHour = timeDifferenceSeconds / 3600;
  // print("Late hour: ${lateHour.toStringAsFixed(1)}");
  final penalty = (lateHour ~/ 2) + 1;
  return -(penalty.clamp(0, 3));
}
