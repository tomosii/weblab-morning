class CheckInException implements Exception {
  final String message;
  CheckInException(this.message);

  @override
  String toString() {
    return "CheckInException(message: $message)";
  }
}

class UserNotFoundException implements Exception {
  UserNotFoundException();
}

class AlreadyCheckedInException implements Exception {
  AlreadyCheckedInException();
}

class InvalidIpAddressException implements Exception {
  InvalidIpAddressException();
}

class InvalidPlaceException implements Exception {
  InvalidPlaceException();
}

class NotCommittedException implements Exception {
  NotCommittedException();
}

class OutOfHoursException implements Exception {
  OutOfHoursException();
}
