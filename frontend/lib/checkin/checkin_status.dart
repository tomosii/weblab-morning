enum NetworkStatus {
  invalid,
  valid,
}

enum LocationStatus {
  withinRange,
  outOfRange,
  notAvailable,
  mocking,
}

enum CheckInProcessStatus {
  notStarted,
  fetchingNetwork,
  fetchingLocation,
  connectingToServer,
  done,
}

class NetworkDetail {
  final String ipAddress;
  final String name;
  final NetworkStatus status;

  NetworkDetail({
    required this.ipAddress,
    required this.name,
    required this.status,
  });
}

class LocationDetail {
  final double distance;
  final String name;
  final LocationStatus status;

  LocationDetail({
    required this.distance,
    required this.name,
    required this.status,
  });
}
