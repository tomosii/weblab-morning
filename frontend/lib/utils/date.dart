import 'package:holiday_jp/holiday_jp.dart' as holiday_jp;

String getJPDayOfWeekString(int dayOfWeek) {
  switch (dayOfWeek) {
    case 1:
      return '月';
    case 2:
      return '火';
    case 3:
      return '水';
    case 4:
      return '木';
    case 5:
      return '金';
    case 6:
      return '土';
    case 7:
      return '日';
    default:
      return '';
  }
}

bool isJPWeekday(DateTime date) {
  final isHoliday = holiday_jp.isHoliday(date);
  return date.weekday <= DateTime.friday && !isHoliday;
}

bool isSameDate(DateTime date1, DateTime date2) {
  return date1.year == date2.year &&
      date1.month == date2.month &&
      date1.day == date2.day;
}

/// 開催中なら開催中の日付を、開催中でなければ次の開催日を返す
List<DateTime> getOngoingOrComingWeekdays() {
  final today = DateTime.now();

  // 今週の月曜日から金曜日のうち、平日の日付を取得
  final thisMonday = today.subtract(Duration(days: today.weekday - 1));
  List<DateTime> thisWeekdays = [];
  for (int i = 0; i < 5; i++) {
    final date = thisMonday.add(Duration(days: i));
    if (isJPWeekday(date)) {
      thisWeekdays.add(date);
    }
  }
  // print("This weekdays: $thisWeekdays");

  // 今週の開催がまだ終わっていなければ、今週の開催日を返す
  if (thisWeekdays.isNotEmpty &&
      (today.isBefore(thisWeekdays.last) ||
          today.isAtSameMomentAs(thisWeekdays.last))) {
    return thisWeekdays;
  }

  // 今週の開催が終わっている場合は、次回の開催日を返す
  final nextMonday = thisMonday.add(Duration(days: 7));
  List<DateTime> nextWeekdays = [];
  for (int i = 0; i < 5; i++) {
    final date = nextMonday.add(Duration(days: i));
    if (isJPWeekday(date)) {
      nextWeekdays.add(date);
    }
  }
  // print("Next weekdays: $nextWeekdays");
  return nextWeekdays;
}
