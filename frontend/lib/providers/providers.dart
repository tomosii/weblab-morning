import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:geolocator/geolocator.dart';

import '../models/place.dart';
import '../checkin/checkin_verification.dart';
import '../checkin/checkin_status.dart';
import '../models/user.dart';
import '../repository/checkin.dart';
import '../repository/user.dart';
import '../utils/ip_address.dart';
import '../utils/location.dart';

final userEmailProvider = StateProvider<String?>((ref) {
  return null;
});

final userProvider = FutureProvider<User?>((ref) async {
  final email = ref.watch(userEmailProvider);
  if (email != null) {
    final userRepository = ref.watch(userRepositoryProvider);
    final user = await userRepository.getUser(email);
    return user;
  }
  return null;
});

final localEmailProvider = FutureProvider<String?>((ref) async {
  final prefs = await SharedPreferences.getInstance();
  String? email = prefs.getString("email");
  print("Email in local storage: $email");

  if (email != null) {
    // SharedPreferenceに上書き（Webストレージの日時を更新）
    await prefs.setString("email", email);
    ref.read(userEmailProvider.notifier).state = email;
  }
  return email;
});

final checkInPlacesProvider =
    FutureProvider.autoDispose<List<CheckInPlace>>((ref) async {
  final db = FirebaseFirestore.instance;
  try {
    final snapshot =
        await db.collection("places").where("enabled", isEqualTo: true).get();
    final places = snapshot.docs.map((e) {
      return CheckInPlace.fromSnapshot(e);
    }).toList();
    print("チェックイン場所を取得: $places");
    return places;
  } catch (e) {
    print("チェックイン場所の取得に失敗: $e");
    rethrow;
  }
});

final currentIpAddressProvider = FutureProvider<String>((ref) async {
  return getIPAddress();
});

final currentPositionProvider = FutureProvider<Position?>((ref) async {
  return getCurrentPosition();
});

final networkDetailProvider =
    FutureProvider.autoDispose<NetworkDetail>((ref) async {
  final checkInPlaces = await ref.watch(checkInPlacesProvider.future);
  final currentIpAddress = await ref.watch(currentIpAddressProvider.future);

  NetworkDetail detail =
      await getNetworkDetail(currentIpAddress, checkInPlaces);
  return detail;
});

final locationDetailProvider =
    FutureProvider.autoDispose<LocationDetail>((ref) async {
  final checkInPlaces = await ref.watch(checkInPlacesProvider.future);
  final currentPosition = await ref.watch(currentPositionProvider.future);

  LocationDetail detail =
      await getLocationDetail(currentPosition, checkInPlaces);
  return detail;
});

final isCheckInAvailableProvider =
    FutureProvider.autoDispose<bool>((ref) async {
  final networkDetail = await ref.watch(networkDetailProvider.future);
  final locationDetail = await ref.watch(locationDetailProvider.future);

  if (networkDetail.status == NetworkStatus.valid &&
      locationDetail.status == LocationStatus.withinRange) {
    ref.read(checkInButtonRippleOpacityProvider.notifier).state = 1.0;
    return true;
  } else {
    ref.read(checkInButtonRippleOpacityProvider.notifier).state = 0.0;
    return false;
  }
});

final checkInButtonRippleOpacityProvider = StateProvider<double>((ref) {
  return 0.0;
});

final checkInResultProvider = StateProvider<CheckInResult>((ref) {
  return CheckInResult();
});

final checkInProcessStatusProvider = StateProvider<CheckInProcessStatus>((ref) {
  return CheckInProcessStatus.notStarted;
});

final appVersionProvider = FutureProvider.autoDispose<String>((ref) async {
  final packageInfo = await PackageInfo.fromPlatform();
  return packageInfo.version;
});
