class DateStatus {
  final DateTime date;
  final bool commitEnabled;
  final bool isWeekday;
  final String? time;
  final int? point;

  DateStatus({
    required this.date,
    this.commitEnabled = true,
    this.isWeekday = true,
    this.time,
    this.point,
  });

  @override
  String toString() {
    return "DateStatus: $date, $commitEnabled, $isWeekday, $time, $point";
  }
}
