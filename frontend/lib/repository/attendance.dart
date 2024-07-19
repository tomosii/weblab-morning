import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:intl/intl.dart';

import '../models/attendance.dart';

final attendanceRepositoryProvider = Provider((ref) => AttendanceRepository());

class AttendanceRepository {
  final _ref = FirebaseFirestore.instance.collection("attendances");

  Future<Attendance?> getAttendance(String userId, DateTime date) async {
    final dateString = DateFormat("yyyy-MM-dd").format(date);

    final doc = await _ref.doc(dateString).get();
    if (!doc.exists) {
      return null;
    }
    final dataMap = doc.data() as Map<String, dynamic>;

    for (final entry in dataMap.entries) {
      if (entry.key == userId) {
        final data = entry.value as Map<String, dynamic>;
        return Attendance(
          userId: userId,
          userName: data["userName"],
          date: date,
          checkInAt: (data["checkInAt"] as Timestamp).toDate(),
          commitmentTime: data["commitmentTime"],
          ipAddress: data["ipAddress"],
          latLng: data["latLng"],
          placeName: data["placeName"],
          timeDifferenceSeconds: data["timeDifferenceSeconds"],
        );
      }
    }

    return null;
  }

  Future<List<Attendance>> getUserAttendances(
      String userId, List<DateTime> dates) async {
    List<Attendance> userAttendances = [];

    for (final date in dates) {
      final attendance = await getAttendance(userId, date);
      if (attendance != null) {
        userAttendances.add(attendance);
      }
    }

    debugPrint("Get ${userAttendances.length} attendances");

    return userAttendances;
  }
}
