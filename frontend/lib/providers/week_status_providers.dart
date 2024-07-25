import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/attendance.dart';
import '../models/commitment.dart';
import '../models/date_status.dart';
import '../repository/attendance.dart';
import '../repository/commitment.dart';
import '../utils/date.dart';
import '../utils/point.dart';
import 'providers.dart';

final thisWeekCommitmentsProvider =
    FutureProvider.autoDispose<UserCommitment?>((ref) async {
  final commitRepository = ref.watch(commitmentRepositoryProvider);
  final user = await ref.watch(userProvider.future);

  if (user != null) {
    final weekdays = getOngoingOrComingWeekdays();
    final userCommitment =
        await commitRepository.getUserCommitment(user.id, weekdays);
    return userCommitment;
  }
});

final thisWeekAttendancesProvider =
    FutureProvider.autoDispose<List<Attendance>?>((ref) async {
  final attendanceRepository = ref.watch(attendanceRepositoryProvider);
  final user = await ref.watch(userProvider.future);

  if (user != null) {
    final weekdays = getOngoingOrComingWeekdays();
    final userAttendances =
        await attendanceRepository.getUserAttendances(user.id, weekdays);
    return userAttendances;
  }
});

final thisWeekStatusProvider =
    FutureProvider.autoDispose<List<DateStatus>?>((ref) async {
  try {
    final weekdays = getOngoingOrComingWeekdays();

    final userCommitment = await ref.watch(thisWeekCommitmentsProvider.future);
    final attendances = await ref.watch(thisWeekAttendancesProvider.future);

    if (userCommitment == null) {
      return null;
    }

    if (userCommitment.dates!.length > 5 || weekdays.length > 5) {
      throw Exception("Too many days in a week");
    }

    List<DateStatus> dateStatusList = [];
    // 月〜金まで
    for (var i = 1; i <= 5; i++) {
      DateTime? currentDate;

      // 開催日かどうかをチェック
      bool isWeekday = false;
      for (var weekday in weekdays) {
        if (weekday.weekday == i) {
          isWeekday = true;
          currentDate = weekday;
          break;
        }
      }
      if (!isWeekday) {
        // 開催日でない場合は空白を追加
        dateStatusList.add(DateStatus(
          date: DateTime(0),
          time: userCommitment.time,
          isWeekday: false,
        ));
        continue;
      }

      // 参加日かどうかをチェック
      bool commitEnabled = false;
      int? pointChange;
      for (var commitDate in userCommitment.dates!) {
        if (isSameDate(currentDate!, commitDate)) {
          commitEnabled = true;
          break;
        }
      }

      // チェックイン結果がある場合はポイントを計算
      if (attendances != null) {
        for (final attendance in attendances) {
          if (isSameDate(currentDate!, attendance.date!)) {
            pointChange = getPointChange(attendance.timeDifferenceSeconds!);
          }
        }
      }

      if (commitEnabled) {
        // 参加日の場合
        dateStatusList.add(
          DateStatus(
            date: currentDate!,
            commitEnabled: true,
            time: userCommitment.time,
            point: pointChange,
          ),
        );
      } else {
        // 参加日でない場合は空白を追加
        dateStatusList.add(DateStatus(
          date: currentDate!,
          time: userCommitment.time,
          commitEnabled: false,
        ));
      }
    }

    return dateStatusList;
  } catch (e) {
    debugPrint("Failed to get this week status: $e");
    rethrow;
  }
});
