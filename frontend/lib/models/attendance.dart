import 'package:cloud_firestore/cloud_firestore.dart';

class Attendance {
  final String? userId;
  final String? userName;
  final DateTime? date;
  final DateTime? checkInAt;
  final String? commitmentTime;
  final String? ipAddress;
  final GeoPoint? latLng;
  final String? placeName;
  final double? timeDifferenceSeconds;

  Attendance({
    this.userId,
    this.userName,
    this.date,
    this.checkInAt,
    this.commitmentTime,
    this.ipAddress,
    this.latLng,
    this.placeName,
    this.timeDifferenceSeconds,
  });

  @override
  String toString() {
    return "Attendance: $userId, $userName, $date, $commitmentTime, $timeDifferenceSeconds";
  }
}
