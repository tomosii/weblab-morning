import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/user.dart';

final userRepositoryProvider = Provider((ref) {
  return UserRepository();
});

class UserRepository {
  final _ref = FirebaseFirestore.instance.collection("users");

  Future<User?> getUser(String email) async {
    final snapshot = await _ref.doc(email).get();
    if (!snapshot.exists) {
      return null;
    }

    final data = snapshot.data();
    if (data == null) {
      return null;
    }

    final user = User(
      id: data["id"],
      email: data["email"],
      nickname: data["nickname"],
    );

    print("Get user: $user");

    return user;
  }
}
