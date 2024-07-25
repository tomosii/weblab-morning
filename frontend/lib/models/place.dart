import 'package:cloud_firestore/cloud_firestore.dart';

class CheckInPlace {
  final String id;
  final String name;
  final List<String> ipAddresses;
  final GeoPoint latLng;

  CheckInPlace({
    required this.id,
    required this.name,
    required this.ipAddresses,
    required this.latLng,
  });

  factory CheckInPlace.fromSnapshot(QueryDocumentSnapshot snapshot) {
    final data = snapshot.data() as Map<String, dynamic>;
    return CheckInPlace(
      id: snapshot.id,
      name: data["name"],
      ipAddresses: List<String>.from(data["ipAddresses"]),
      latLng: data["latLng"],
    );
  }

  @override
  String toString() {
    return "CheckInPlace(id: $id, name: $name, ipAddresses: $ipAddresses, latLng: $latLng)";
  }
}
