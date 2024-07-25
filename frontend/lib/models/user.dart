class User {
  final String id;
  final String email;
  final String nickname;

  User({
    required this.id,
    required this.email,
    required this.nickname,
  });

  @override
  String toString() {
    return "User: $id, $email, $nickname";
  }
}
