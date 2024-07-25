import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:loading_animation_widget/loading_animation_widget.dart';

import 'package:morning_web/checkin/checkin_status.dart';
import 'package:morning_web/providers/providers.dart';
import '../../constants/colors.dart';

class CheckInLoadingPage extends ConsumerStatefulWidget {
  const CheckInLoadingPage({super.key});

  @override
  ConsumerState<CheckInLoadingPage> createState() => _CheckInLoadingPageState();
}

class _CheckInLoadingPageState extends ConsumerState<CheckInLoadingPage> {
  late final Timer _timer;

  double _titleOpacity = 0;

  LinearGradient _bgGradient = const LinearGradient(
    colors: [
      morningBlue,
      morningBlue,
      // Colors.green,
      // Colors.green,
    ],
  );

  final List<LinearGradient> _gradients = [
    const LinearGradient(
      colors: [
        morningBlue,
        Color(0xFF3DAFE0),
      ],
      begin: Alignment.topLeft,
      end: Alignment.bottomRight,
    ),
    const LinearGradient(
      colors: [
        morningBlue,
        Color(0xFF3DAFE0),
      ],
      begin: Alignment.topRight,
      end: Alignment.bottomLeft,
    ),
    const LinearGradient(
      colors: [
        morningBlue,
        Color(0xFF3D74E0),
      ],
      begin: Alignment.bottomRight,
      end: Alignment.topLeft,
    ),
    const LinearGradient(
      colors: [
        morningBlue,
        Color(0xFF3D74E0),
      ],
      begin: Alignment.bottomLeft,
      end: Alignment.topRight,
    ),
    // == Christmas ==
    // LinearGradient(
    //   colors: [
    //     Colors.green[800]!,
    //     Colors.green,
    //   ],
    //   begin: Alignment.topLeft,
    //   end: Alignment.bottomRight,
    // ),
    // LinearGradient(
    //   colors: [
    //     Colors.green,
    //     Colors.green[800]!,
    //   ],
    //   begin: Alignment.topRight,
    //   end: Alignment.bottomLeft,
    // ),
    // const LinearGradient(
    //   colors: [
    //     Colors.green,
    //     Colors.greenAccent,
    //   ],
    //   begin: Alignment.bottomRight,
    //   end: Alignment.topLeft,
    // ),
    // const LinearGradient(
    //   colors: [
    //     Colors.green,
    //     Colors.greenAccent,
    //   ],
    //   begin: Alignment.bottomLeft,
    //   end: Alignment.topRight,
    // ),
  ];

  @override
  void initState() {
    super.initState();

    Future.delayed(const Duration(milliseconds: 0), () {
      setState(() {
        _bgGradient = _gradients.last;
      });
    });

    _timer = Timer.periodic(const Duration(milliseconds: 400), (timer) {
      setState(() {
        _bgGradient = _gradients[timer.tick % _gradients.length];
      });
    });

    Future.delayed(const Duration(milliseconds: 0), () {
      setState(() {
        _titleOpacity = 1;
      });
    });
  }

  @override
  void dispose() {
    _timer.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final status = ref.watch(checkInProcessStatusProvider);

    return Scaffold(
      backgroundColor: morningBlue,
      body: AnimatedContainer(
        duration: const Duration(milliseconds: 500),
        decoration: BoxDecoration(
          gradient: _bgGradient,
        ),
        child: Center(
          // heightFactor: 1.0,
          child: Container(
            // alignment: Alignment.topCenter,
            constraints: const BoxConstraints(
              maxWidth: 400,
            ),
            padding: const EdgeInsets.symmetric(
              horizontal: 28,
            ),
            child: Container(
              // margin: const EdgeInsets.only(top: 120),
              // height: 200,
              child: Column(
                // mainAxisAlignment: MainAxisAlignment.spaceBetween,
                // crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  AnimatedOpacity(
                    duration: const Duration(milliseconds: 600),
                    opacity: _titleOpacity,
                    child: const Text(
                      "チェックインしています",
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 20,
                        fontWeight: FontWeight.w800,
                      ),
                    ),
                  ),
                  const SizedBox(
                    height: 70,
                  ),
                  AnimatedOpacity(
                    duration: const Duration(milliseconds: 600),
                    opacity: _titleOpacity,
                    child: LoadingAnimationWidget.fourRotatingDots(
                      color: Colors.white,
                      size: 55,
                    ),
                  ),
                  const SizedBox(
                    height: 100,
                  ),
                  // _statusRow(
                  //   text: "IPアドレスを取得中...",
                  //   loading: status.index >=
                  //       CheckInProcessStatus.fetchingNetwork.index,
                  //   done: status.index >
                  //       CheckInProcessStatus.fetchingNetwork.index,
                  //   // completeWidget: Transform.rotate(
                  //   //   angle: -0.2,
                  //   //   child: Image.asset(
                  //   //     "assets/images/christmas-ball1.png",
                  //   //     width: 24,
                  //   //   ),
                  //   // ),
                  // ),
                  // _statusRow(
                  //   text: "現在地を取得中...",
                  //   loading: status.index >=
                  //       CheckInProcessStatus.fetchingLocation.index,
                  //   done: status.index >
                  //       CheckInProcessStatus.fetchingLocation.index,
                  //   // completeWidget: Transform.rotate(
                  //   //   angle: 0.5,
                  //   //   child: Image.asset(
                  //   //     "assets/images/christmas-ball2.png",
                  //   //     width: 24,
                  //   //   ),
                  //   // ),
                  // ),
                  // _statusRow(
                  //   text: "サーバーと通信中...",
                  //   loading: status.index >=
                  //       CheckInProcessStatus.connectingToServer.index,
                  //   done: status.index >
                  //       CheckInProcessStatus.connectingToServer.index,
                  //   // completeWidget: Transform.rotate(
                  //   //   angle: -0.1,
                  //   //   child: Image.asset(
                  //   //     "assets/images/christmas-ball3.png",
                  //   //     width: 24,
                  //   //   ),
                  //   // ),
                  // ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _statusRow({
    required String text,
    required bool loading,
    required bool done,
    Widget? completeWidget,
  }) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        AnimatedOpacity(
          opacity: done ? 1 : 0,
          duration: const Duration(milliseconds: 400),
          child: completeWidget ??
              Icon(
                Icons.check_rounded,
                color: Colors.white.withOpacity(0.7),
                size: 24,
              ),
        ),
        const SizedBox(
          width: 20,
        ),
        AnimatedOpacity(
          opacity: loading ? 1 : 0,
          duration: const Duration(milliseconds: 500),
          child: Text(
            text,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 15,
              fontWeight: FontWeight.w600,
            ),
          ),
        ),
      ],
    );
  }
}
