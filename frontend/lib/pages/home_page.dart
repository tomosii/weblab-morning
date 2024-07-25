import 'dart:ui';
import 'dart:math';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:geolocator/geolocator.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:morning_web/checkin/checkin_verification.dart';
import 'package:morning_web/pages/loading_page.dart';
import 'package:morning_web/providers/providers.dart';
import 'package:morning_web/providers/week_status_providers.dart';
import 'package:morning_web/repository/commitment.dart';
import 'package:morning_web/utils/ip_address.dart';
import 'package:morning_web/utils/location.dart';
import 'package:morning_web/checkin/checkin_status.dart';
import 'package:morning_web/utils/screen_size.dart';
import 'package:sprung/sprung.dart';

import '../../constants/colors.dart';
import '../components/date_status.dart';
import '../components/ripple_animation.dart';
import '../models/date_status.dart';
import '../utils/date.dart';

class HomePage extends ConsumerStatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  ConsumerState<HomePage> createState() => _HomePageState();
}

class _HomePageState extends ConsumerState<HomePage>
    with TickerProviderStateMixin {
  double _headerOpacity = 0;
  double _bgOpacity = 0;
  double _statusOpacity = 0;
  double _buttonOpacity = 0;

  double _statusPanelScale = 0;

  bool _checkInLoading = false;

  late final AnimationController _bottonRippleAnimController;
  late final AnimationController _rippleTransitionAnimController;
  late final Animation<double> _rippleTransitionAnimation;

  @override
  void initState() {
    super.initState();
    _bottonRippleAnimController = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    )..repeat();

    _rippleTransitionAnimController = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );
    _rippleTransitionAnimation = Tween<double>(
      begin: 0,
      end: max(ScreenSize.width, ScreenSize.height) * 2,
    ).animate(
      CurvedAnimation(
        parent: _rippleTransitionAnimController,
        curve: Curves.easeInOutCirc,
      ),
    );

    Future.delayed(const Duration(milliseconds: 500), () {
      setState(() {
        _headerOpacity = 1;
        _bgOpacity = 0.4;
      });
    });

    Future.delayed(const Duration(milliseconds: 1000), () {
      setState(() {
        _statusOpacity = 1;
        _statusPanelScale = 1;
      });
    });

    Future.delayed(const Duration(milliseconds: 1500), () {
      setState(() {
        _buttonOpacity = 1;
      });
    });
  }

  @override
  void dispose() {
    _bottonRippleAnimController.dispose();
    _rippleTransitionAnimController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        heightFactor: 1,
        child: Stack(
          clipBehavior: Clip.none,
          alignment: Alignment.topCenter,
          children: [
            // Positioned(
            //   right: -150,
            //   top: -120,
            //   child: AnimatedOpacity(
            //     duration: const Duration(milliseconds: 1000),
            //     opacity: _bgOpacity,
            //     child: Image.asset(
            //       "assets/images/yellow-circle.png",
            //       width: 280,
            //       height: 280,
            //     ),
            //   ),
            // ),
            BackdropFilter(
              filter: ImageFilter.blur(
                sigmaX: 24,
                sigmaY: 24,
              ),
              child: RefreshIndicator(
                onRefresh: () async {
                  // 再取得
                  ref.invalidate(currentIpAddressProvider);
                  ref.invalidate(currentPositionProvider);
                  ref.invalidate(thisWeekCommitmentsProvider);
                  ref.invalidate(thisWeekAttendancesProvider);
                  await Future.delayed(const Duration(milliseconds: 700));
                },
                child: SingleChildScrollView(
                  clipBehavior: Clip.none,
                  physics: const AlwaysScrollableScrollPhysics(),
                  padding: EdgeInsets.zero,
                  child: Container(
                    alignment: Alignment.topCenter,
                    constraints: const BoxConstraints(
                      maxWidth: 400,
                    ),
                    padding: const EdgeInsets.symmetric(
                      horizontal: 24,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const SizedBox(
                          height: 10,
                        ),
                        _logo(),
                        const SizedBox(
                          height: 12,
                        ),
                        _currentDateAndTime(),
                        const SizedBox(
                          height: 25,
                        ),
                        _checkInStatusPanel(),
                        const SizedBox(
                          height: 20,
                        ),
                        _thisWeekStatusPanel(),
                        const SizedBox(
                          height: 100,
                        ),
                        _showCheckInButton(),
                        const SizedBox(
                          height: 100,
                        ),
                        _debugInfo(),
                        const SizedBox(
                          height: 30,
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _logo() {
    final appVersion = ref.watch(appVersionProvider);
    return AnimatedOpacity(
      duration: const Duration(milliseconds: 1600),
      opacity: _headerOpacity,
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          Image.asset(
            'assets/images/morning-logo.png',
            height: 45,
            // "assets/images/morning-logo-christmas.png",
            // height: 70,
          ),
          const SizedBox(
            width: 10,
          ),
          Container(
            decoration: BoxDecoration(
              color: morningBgBlue,
              borderRadius: BorderRadius.circular(5),
            ),
            padding: const EdgeInsets.symmetric(
              horizontal: 9,
              vertical: 5,
            ),
            margin: const EdgeInsets.only(bottom: 8),
            child: Text(
              appVersion.when(
                data: (version) => version,
                loading: () => "0.0.0",
                error: (error, stackTrace) => "0.0.0",
              ),
              style: GoogleFonts.inter(
                color: morningFgBlue,
                fontWeight: FontWeight.w400,
                fontSize: 11,
                height: 1.0,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _currentDateAndTime() {
    return AnimatedOpacity(
      duration: const Duration(milliseconds: 1600),
      opacity: _headerOpacity,
      child: StreamBuilder<DateTime>(
        stream: Stream.periodic(
            const Duration(milliseconds: 100), (_) => DateTime.now()),
        builder: (BuildContext context, AsyncSnapshot<DateTime> snap) {
          if (snap.hasData) {
            final DateTime now = snap.data!;
            return Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  "${now.year}年${now.month}月${now.day}日 (${getJPDayOfWeekString(now.weekday)})",
                  style: TextStyle(
                    fontFamily: "Inter",
                    fontSize: 14,
                    fontWeight: FontWeight.w500,
                    color: Colors.black.withOpacity(0.4),
                    letterSpacing: 1.1,
                  ),
                ),
                const SizedBox(
                  height: 2,
                ),
                Text(
                  "${now.hour.toString().padLeft(2, '0')}:${now.minute.toString().padLeft(2, '0')}:${now.second.toString().padLeft(2, '0')}",
                  style: TextStyle(
                    fontFamily: "Inter",
                    fontSize: 32,
                    fontWeight: FontWeight.w700,
                    color: Colors.black.withOpacity(0.7),
                  ),
                ),
              ],
            );
          } else if (snap.hasError) {
            return Text("Error: ${snap.error}");
          } else {
            return Container();
          }
        },
      ),
    );
  }

  Widget _checkInStatusPanel() {
    return AnimatedScale(
      duration: const Duration(milliseconds: 1700),
      scale: _statusPanelScale,
      curve: Sprung.overDamped,
      child: AnimatedOpacity(
        duration: const Duration(milliseconds: 800),
        opacity: _statusOpacity,
        child: Center(
          child: Container(
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: const BorderRadius.all(Radius.circular(14)),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.08),
                  blurRadius: 35,
                  offset: const Offset(0, 0),
                  spreadRadius: 1,
                ),
              ],
            ),
            padding: const EdgeInsets.symmetric(
              horizontal: 24,
              vertical: 20,
            ),
            child: Column(
              children: [
                ref.watch(networkDetailProvider).when(
                      data: (networkDetail) {
                        if (networkDetail.status == NetworkStatus.valid) {
                          return _checkInStatusRow(
                            icon: Icons.wifi_rounded,
                            color: morningBlue,
                            text: "指定のネットワークに接続されています",
                            detail: networkDetail.name,
                          );
                        } else {
                          return _checkInStatusRow(
                            icon: Icons.wifi_off_rounded,
                            color: morningPink,
                            text: "指定のネットワークに接続されていません",
                          );
                        }
                      },
                      loading: () => _checkInStatusRow(
                        icon: Icons.wifi,
                        color: Colors.black.withOpacity(0.2),
                        text: "ネットワーク情報を取得中...",
                      ),
                      error: (error, stackTrace) => _checkInStatusRow(
                        icon: Icons.wifi_off_rounded,
                        color: morningPink,
                        text: "ネットワーク情報を取得できませんでした",
                      ),
                    ),
                const SizedBox(
                  height: 12,
                ),
                ref.watch(locationDetailProvider).when(
                      data: (locationDetail) {
                        if (locationDetail.status ==
                            LocationStatus.withinRange) {
                          final name = locationDetail.name;
                          final distance = locationDetail.distance.toInt();
                          return _checkInStatusRow(
                            icon: Icons.gps_fixed,
                            color: morningBlue,
                            text: "チェックインエリア圏内です",
                            detail: "$name から${distance}m",
                          );
                        } else if (locationDetail.status ==
                            LocationStatus.outOfRange) {
                          return _checkInStatusRow(
                            icon: Icons.gps_off,
                            color: morningPink,
                            text: "チェックインエリア圏外です",
                          );
                        } else if (locationDetail.status ==
                            LocationStatus.notAvailable) {
                          return _checkInStatusRow(
                            icon: Icons.location_disabled_rounded,
                            color: morningPink,
                            text: "位置情報を取得できませんでした",
                          );
                        } else if (locationDetail.status ==
                            LocationStatus.mocking) {
                          return _checkInStatusRow(
                            icon: Icons.location_disabled_rounded,
                            color: morningPink,
                            text: "位置情報が偽装されています",
                          );
                        } else {
                          return _checkInStatusRow(
                            icon: Icons.location_disabled_rounded,
                            color: morningPink,
                            text: "位置情報を取得できませんでした",
                          );
                        }
                      },
                      loading: () => _checkInStatusRow(
                        icon: Icons.gps_not_fixed,
                        color: Colors.black.withOpacity(0.2),
                        text: "位置情報を取得中...",
                      ),
                      error: (error, stackTrace) => _checkInStatusRow(
                        icon: Icons.location_disabled_rounded,
                        color: morningPink,
                        text: "位置情報を取得できませんでした",
                      ),
                    ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _checkInStatusRow({
    required IconData icon,
    required Color color,
    required String text,
    String? detail,
  }) {
    return Row(
      children: [
        Icon(
          icon,
          size: 21,
          color: color,
        ),
        const SizedBox(
          width: 15,
        ),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                text,
                style: TextStyle(
                  fontSize: 12,
                  fontWeight: FontWeight.w500,
                  color: Colors.black.withOpacity(0.65),
                ),
              ),
              if (detail != null) ...[
                const SizedBox(
                  height: 3,
                ),
                Text(
                  detail,
                  style: TextStyle(
                    fontSize: 10,
                    fontWeight: FontWeight.w500,
                    color: Colors.black.withOpacity(0.4),
                  ),
                ),
              ],
            ],
          ),
        ),
      ],
    );
  }

  Widget _showCheckInButton() {
    return Stack(
      alignment: Alignment.center,
      children: [
        AnimatedOpacity(
          duration: const Duration(milliseconds: 1400),
          opacity: _buttonOpacity,
          child: Stack(
            children: [
              Positioned.fill(
                child: AnimatedOpacity(
                  duration: const Duration(milliseconds: 2500),
                  opacity: ref.watch(checkInButtonRippleOpacityProvider),
                  child: CustomPaint(
                    painter: CircleRipplePainter(
                      _bottonRippleAnimController,
                      color: morningBlue,
                      // color: Colors.redAccent,
                    ),
                    child: const SizedBox(
                      width: 160,
                      height: 160,
                    ),
                  ),
                ),
              ),
              Align(
                alignment: Alignment.center,
                child: ref.watch(isCheckInAvailableProvider).when(
                      data: (isCheckInAvailable) {
                        if (isCheckInAvailable) {
                          return _checkInButton(true);
                        } else {
                          return _checkInButton(false);
                        }
                      },
                      loading: () => _checkInButton(false),
                      error: (error, stackTrace) => _checkInButton(false),
                    ),
              ),
            ],
          ),
        ),
        // Transition animation of expanding circle
        Align(
          alignment: Alignment.topCenter,
          child: ScaleTransition(
            scale: _rippleTransitionAnimation,
            child: Container(
              width: 1,
              height: 1,
              decoration: const ShapeDecoration(
                shape: CircleBorder(),
                color: morningBlue,
                // color: Colors.green[600]!,
              ),
            ),
          ),
        ),
      ],
    );
  }

  Widget _checkInButton(bool enabled) {
    return Center(
      child: SizedBox(
        width: 160,
        height: 160,
        child: ElevatedButton(
          style: ElevatedButton.styleFrom(
            shape: CircleBorder(
              side: BorderSide(
                color: Colors.black.withOpacity(0.07),
                width: enabled ? 0 : 2,
              ),
            ),
            backgroundColor: Colors.white,
            elevation: 0,
            padding: const EdgeInsets.all(0),
          ),
          onPressed: () {
            if (!enabled || _checkInLoading) {
              return;
            }
            _startCheckInAndPush();
          },
          child: _checkInLoading
              ? const SizedBox(
                  width: 30,
                  height: 30,
                  child: CircularProgressIndicator(
                    color: morningBlue,
                    // color: Colors.green[600]!,
                    strokeWidth: 3,
                  ),
                )
              : Icon(
                  Icons.brightness_7,
                  color: enabled ? morningBlue : Colors.black.withOpacity(0.2),
                  size: 35,
                  // : ClipRect(
                  //     child: ColorFiltered(
                  //       colorFilter: ColorFilter.mode(
                  //         enabled ? Colors.transparent : Colors.white,
                  //         BlendMode.saturation,
                  //       ),
                  //       child: Image.asset(
                  //         "assets/images/bell.png",
                  //         width: 35,
                  //         height: 35,
                  //       ),
                  //     ),
                ),
        ),
      ),
    );
  }

  Widget _debugInfo() {
    return AnimatedOpacity(
      duration: const Duration(milliseconds: 1400),
      opacity: _buttonOpacity,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          FutureBuilder<String>(
            future: getIPAddress(),
            builder: (BuildContext context, AsyncSnapshot<String> snapshot) {
              if (snapshot.hasData) {
                return Text(
                  snapshot.data!,
                  style: TextStyle(
                    fontSize: 9,
                    color: Colors.black.withOpacity(0.3),
                  ),
                );
              } else if (snapshot.hasError) {
                return Text(
                  snapshot.error.toString(),
                  style: TextStyle(
                    fontSize: 9,
                    color: Colors.black.withOpacity(0.3),
                  ),
                );
              }
              return Container();
            },
          ),
          FutureBuilder<Position?>(
            future: getCurrentPosition(),
            builder: (BuildContext context, AsyncSnapshot<Position?> snapshot) {
              if (snapshot.hasData) {
                return Text(
                  "${snapshot.data!.latitude}, ${snapshot.data!.longitude}",
                  style: TextStyle(
                    fontSize: 9,
                    color: Colors.black.withOpacity(0.3),
                  ),
                );
              } else if (snapshot.hasError) {
                return Text(
                  snapshot.error.toString(),
                  style: TextStyle(
                    fontSize: 9,
                    color: Colors.black.withOpacity(0.3),
                  ),
                );
              }
              return Container();
            },
          ),
        ],
      ),
    );
  }

  Widget _thisWeekStatusPanel() {
    return AnimatedScale(
      duration: const Duration(milliseconds: 1700),
      scale: _statusPanelScale,
      curve: Sprung.overDamped,
      child: AnimatedOpacity(
        duration: const Duration(milliseconds: 800),
        opacity: _statusOpacity,
        child: Center(
          child: Container(
            width: double.infinity,
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: const BorderRadius.all(Radius.circular(14)),
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.08),
                  blurRadius: 35,
                  offset: const Offset(0, 0),
                  spreadRadius: 1,
                ),
              ],
            ),
            padding: const EdgeInsets.symmetric(
              horizontal: 18,
              vertical: 20,
            ),
            child: ref.watch(thisWeekStatusProvider).when(
              data: (statusList) {
                if (statusList == null) {
                  return Center(
                    child: Text(
                      "朝活に参加していません",
                      style: TextStyle(
                        fontSize: 12,
                        fontWeight: FontWeight.w500,
                        color: Colors.black.withOpacity(0.4),
                      ),
                    ),
                  );
                }
                return Column(
                  children: [
                    Text(
                      statusList.first.time ?? "",
                      style: TextStyle(
                        fontFamily: "Inter",
                        fontSize: 22,
                        fontWeight: FontWeight.w700,
                        color: Colors.black.withOpacity(0.7),
                      ),
                    ),
                    const SizedBox(
                      height: 15,
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: statusList.map((status) {
                        return DateStatusIndicator(
                          status: status,
                        );
                      }).toList(),
                    ),
                    const SizedBox(
                      height: 3,
                    ),
                  ],
                );
              },
              loading: () {
                return Column(
                  children: [
                    const SizedBox(
                      height: 40,
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: List.generate(5, (index) {
                        return DateStatusIndicator(
                          status: DateStatus(
                            date: DateTime(0),
                            commitEnabled: false,
                          ),
                        );
                      }),
                    ),
                  ],
                );
              },
              error: (error, stackTrace) {
                return Center(
                  child: Text(
                    "エラーが発生しました。",
                    style: TextStyle(
                      fontSize: 12,
                      color: Colors.black.withOpacity(0.4),
                    ),
                  ),
                );
              },
            ),
          ),
        ),
      ),
    );
  }

  Future<void> _startCheckInAndPush() async {
    setState(() {
      _checkInLoading = true;
    });
    ref.read(checkInProcessStatusProvider.notifier).state =
        CheckInProcessStatus.notStarted;

    await Future.delayed(const Duration(milliseconds: 150));

    _rippleTransitionAnimController.forward();

    await Future.delayed(const Duration(milliseconds: 600));

    checkIn(context, ref);

    // Use FadeTransitionn
    Navigator.of(context).push(
      PageRouteBuilder(
        transitionDuration: const Duration(milliseconds: 300),
        pageBuilder: (BuildContext context, animation, secondaryAnimation) {
          return FadeTransition(
            opacity: animation,
            child: const CheckInLoadingPage(),
          );
        },
      ),
    );
    return;
  }
}
