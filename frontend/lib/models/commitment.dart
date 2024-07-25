class Commitment {
  final DateTime? date;
  final String? userId;
  final String? userName;
  final String? time;

  Commitment({
    this.date,
    this.userId,
    this.userName,
    this.time,
  });

  @override
  String toString() {
    return "Commitment: $date, $userId, $userName, $time";
  }
}

class UserCommitment {
  final String? userId;
  final String? userName;
  final String? time;
  final List<DateTime>? dates;

  UserCommitment({
    this.userId,
    this.userName,
    this.time,
    this.dates,
  });

  @override
  String toString() {
    return "UserCommitment: $userId, $userName, $time, $dates";
  }
}
