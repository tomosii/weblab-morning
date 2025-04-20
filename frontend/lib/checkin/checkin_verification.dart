import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:geolocator/geolocator.dart';
import 'package:morning_web/models/place.dart';
import 'package:morning_web/providers/providers.dart';
import 'package:morning_web/utils/ip_address.dart';

import '../components/error_dialog.dart';
import '../providers/week_status_providers.dart';
import '../repository/checkin.dart';
import '../utils/location.dart';
import 'checkin_exception.dart';
import 'checkin_status.dart';

Future<NetworkDetail> getNetworkDetail(
  String currentIpAdress,
  List<CheckInPlace> checkInPlaces,
) async {
  // チェックイン場所のIPアドレスと比較
  for (final place in checkInPlaces) {
    for (final ip in place.ipAddresses) {
      if (currentIpAdress.contains(ip)) {
        print("一致したIPアドレス: $ip (${place.name})");
        final currentPlace = place;
        return NetworkDetail(
          ipAddress: currentIpAdress,
          name: currentPlace.name,
          status: NetworkStatus.valid,
        );
      }
    }
  }
  print("一致するIPアドレス なし");
  return NetworkDetail(
    ipAddress: currentIpAdress,
    name: "",
    status: NetworkStatus.invalid,
  );
}

Future<LocationDetail> getLocationDetail(
  Position? currentPosition,
  List<CheckInPlace> checkInPlaces,
) async {
  if (currentPosition == null) {
    return LocationDetail(
      distance: 0,
      name: "",
      status: LocationStatus.notAvailable,
    );
  }

  // 現在地から各場所までの距離を計算
  final distanceFromGoal = checkInPlaces.map((place) {
    final distance = Geolocator.distanceBetween(
      currentPosition.latitude,
      currentPosition.longitude,
      place.latLng.latitude,
      place.latLng.longitude,
    );
    return distance;
  }).toList();

  print("現在地からの距離: $distanceFromGoal");

  // 最短距離を取得
  final minDistance = distanceFromGoal.reduce(min);
  final minDistancePlace = checkInPlaces[distanceFromGoal.indexOf(minDistance)];

  print("最短距離: $minDistance (${minDistancePlace.name})");

  late LocationStatus status;

  if (minDistance > 30) {
    status = LocationStatus.outOfRange;
  } else {
    status = LocationStatus.withinRange;
  }

  return LocationDetail(
    distance: minDistance,
    name: minDistancePlace.name,
    status: status,
  );
}

Future<void> checkIn(BuildContext context, WidgetRef ref) async {
  try {
    print("Start check-in process...");

    final user = await ref.read(userProvider.future);
    print("Get email from provider: ${user!.email}");

    final ipAddress = await ref.read(currentIpAddressProvider.future);
    print("Get IP address from provider: $ipAddress");

    final currentPosition = await ref.read(currentPositionProvider.future);
    print("Get current position from provider: $currentPosition");

    // await Future.delayed(const Duration(milliseconds: 900));

    // ref.read(checkInProcessStatusProvider.notifier).state =
    //     CheckInProcessStatus.fetchingNetwork;
    // print("IPアドレスを取得中...");
    // final ipAddress = await getIPAddress();

    // await Future.delayed(const Duration(milliseconds: 900));

    // ref.read(checkInProcessStatusProvider.notifier).state =
    //     CheckInProcessStatus.fetchingLocation;
    // print("位置情報を取得中...");
    // final currentPosition = await getCurrentPosition();

    // await Future.delayed(const Duration(milliseconds: 900));

    // ref.read(checkInProcessStatusProvider.notifier).state =
    //     CheckInProcessStatus.connectingToServer;
    // print("サーバーと通信中...");

    // await Future.delayed(const Duration(milliseconds: 900));

    print("Sending check-in request...");
    final result = await CheckInRepository().post(
      user.email,
      ipAddress,
      currentPosition!.latitude,
      currentPosition!.longitude,
    );
    print("Check-in result: $result");

    ref.read(checkInResultProvider.notifier).state = result;
    ref.read(checkInProcessStatusProvider.notifier).state =
        CheckInProcessStatus.done;

    ref.invalidate(thisWeekCommitmentsProvider);
    ref.invalidate(thisWeekAttendancesProvider);

    Navigator.pushNamedAndRemoveUntil(
      context,
      "/result",
      (_) => false,
    );
  } on Exception catch (error) {
    // 再取得
    ref.invalidate(currentIpAddressProvider);
    ref.invalidate(currentPositionProvider);
    ref.invalidate(thisWeekCommitmentsProvider);
    ref.invalidate(thisWeekAttendancesProvider);

    await showDialog(
      context: context,
      builder: (_) {
        switch (error) {
          case UserNotFoundException _:
            return const MorningErrorDialog(
              title: "チェックインに失敗しました",
              message: "ユーザーが見つかりませんでした。",
            );
          case AlreadyCheckedInException _:
            return const MorningErrorDialog(
              title: "チェックインに失敗しました",
              message: "本日は既にチェックイン済みです。",
            );
          case InvalidIpAddressException _:
            return const MorningErrorDialog(
              title: "チェックインに失敗しました",
              message: "IPアドレスが一致しませんでした。",
            );
          case InvalidPlaceException _:
            return const MorningErrorDialog(
              title: "チェックインに失敗しました",
              message: "チェックインエリア外です。",
            );
          case NotCommittedException _:
            return const MorningErrorDialog(
              title: "チェックインに失敗しました",
              message: "本日は朝活に参加していません。",
            );
          case OutOfHoursException _:
            return const MorningErrorDialog(
              title: "チェックインに失敗しました",
              message: "チェックイン可能時間外です。",
            );
          default:
            return MorningErrorDialog(
              title: "チェックインに失敗しました",
              message: "不明なエラーが発生しました。 (${error.toString()})",
            );
        }
      },
    );

    Navigator.pushNamedAndRemoveUntil(
      context,
      "/",
      (_) => false,
    );
  }
}
