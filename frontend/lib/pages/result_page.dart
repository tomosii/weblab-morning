import 'dart:math';

import 'package:confetti/confetti.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:morning_web/components/primary_button.dart';
import 'package:intl/intl.dart';
import 'package:morning_web/providers/providers.dart';
import 'package:sprung/sprung.dart';

import '../../constants/colors.dart';
import '../providers/week_status_providers.dart';

class CheckInResultPage extends ConsumerStatefulWidget {
  const CheckInResultPage({super.key});

  @override
  ConsumerState<CheckInResultPage> createState() => _CheckInResultPageState();
}

class _CheckInResultPageState extends ConsumerState<CheckInResultPage>
    with TickerProviderStateMixin {
  double _placeOpacity = 0;
  double _timeOpacity = 0;
  double _messageOpacity = 0;
  double _imageOpacity = 0;
  double _imageScale = 0;

  late ConfettiController _confettiController;

  final List<String> _images = [
    "assets/images/christmas-tree.png",
    "assets/images/cookie.png",
    "assets/images/sock.png",
    "assets/images/snow-globe.png",
    "assets/images/present.png",
    "assets/images/snow-globe.png",
    "assets/images/cookie.png",
  ];

  int _imageIndex = 0;

  @override
  void initState() {
    super.initState();

    _imageIndex = DateTime.now().weekday - 1;
    if (_imageIndex >= _images.length) {
      _imageIndex = 0;
    }

    _confettiController =
        ConfettiController(duration: const Duration(milliseconds: 1200));
    Future.delayed(const Duration(milliseconds: 1000), () {
      _confettiController.play();
    });

    Future.delayed(const Duration(milliseconds: 300), () {
      setState(() {
        _placeOpacity = 1;
      });
    });

    Future.delayed(const Duration(milliseconds: 900), () {
      setState(() {
        _timeOpacity = 1;
      });
    });

    Future.delayed(const Duration(milliseconds: 1500), () {
      setState(() {
        _messageOpacity = 1;
      });
    });

    Future.delayed(const Duration(milliseconds: 2000), () {
      setState(() {
        _imageOpacity = 1;
        _imageScale = 1;
      });
    });
  }

  @override
  void dispose() {
    _confettiController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final checkInResult = ref.watch(checkInResultProvider);
    return Scaffold(
      backgroundColor: Colors.white,
      body: Center(
        child: Container(
          alignment: Alignment.topCenter,
          constraints: const BoxConstraints(
            maxWidth: 400,
          ),
          padding: const EdgeInsets.symmetric(
            horizontal: 28,
          ),
          child: Column(
            children: [
              const SizedBox(
                height: 20,
              ),
              if ((checkInResult.timeDifferenceSeconds ?? 0) <= 0)
                ConfettiWidget(
                  confettiController: _confettiController,
                  numberOfParticles: 6,
                  emissionFrequency: 0.07,
                  blastDirectionality: BlastDirectionality.directional,
                  blastDirection: -pi / 2,
                  shouldLoop: false,
                  maxBlastForce: 10,
                  colors: [
                    morningBlue,
                    Colors.amber[200]!,
                    // Colors.orange[200]!,
                    // Colors.green,
                    // Colors.red,
                  ],
                ),
              Container(
                alignment: Alignment.centerRight,
                // fromat current datetime
                child: Text(
                  DateFormat("yyyy/MM/dd HH:mm").format(DateTime.now()),
                  style: const TextStyle(
                    fontFamily: "Inter",
                    fontSize: 14,
                    fontWeight: FontWeight.w400,
                    color: Colors.grey,
                  ),
                ),
              ),
              const SizedBox(
                height: 40,
              ),
              AnimatedOpacity(
                duration: const Duration(milliseconds: 1000),
                opacity: _placeOpacity,
                child: Column(
                  children: [
                    const Icon(
                      Icons.place,
                      size: 47,
                      color: morningBlue,
                    ),
                    const SizedBox(
                      height: 5,
                    ),
                    Text(
                      checkInResult.placeName ?? "None",
                      style: GoogleFonts.montserrat(
                        fontSize: 47,
                        fontWeight: FontWeight.w700,
                        color: Colors.black,
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(
                height: 15,
              ),
              AnimatedOpacity(
                duration: const Duration(milliseconds: 1000),
                opacity: _timeOpacity,
                child: Text(
                  _parseTimeDifference(
                      checkInResult.timeDifferenceSeconds ?? 0),
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.w800,
                    color: ((checkInResult.timeDifferenceSeconds ?? 0) < 0)
                        ? morningBlue
                        : morningPink,
                  ),
                ),
              ),
              // const SizedBox(
              //   height: 30,
              // ),
              // AnimatedScale(
              //   duration: const Duration(milliseconds: 2600),
              //   scale: _imageScale,
              //   curve: Sprung.overDamped,
              //   child: AnimatedOpacity(
              //     duration: const Duration(milliseconds: 1000),
              //     opacity: _imageOpacity,
              //     child: Transform.rotate(
              //       angle: -0.15,
              //       child: Image.asset(
              //         _images[_imageIndex],
              //         height: 140,
              //       ),
              //     ),
              //   ),
              // ),
              const SizedBox(
                height: 40,
              ),
              AnimatedOpacity(
                duration: const Duration(milliseconds: 1000),
                opacity: _messageOpacity,
                child: Column(
                  children: [
                    Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        ref.watch(userProvider).maybeWhen(
                              data: (user) {
                                return Text(
                                  "${user!.nickname}さん、おはようございます。",
                                  style: TextStyle(
                                      fontSize: 18,
                                      fontWeight: FontWeight.w900,
                                      color: Colors.black.withOpacity(0.8)),
                                );
                              },
                              orElse: () => const SizedBox(),
                            ),
                        const SizedBox(
                          height: 10,
                        ),
                        Text(
                          _message(checkInResult.timeDifferenceSeconds ?? 0),
                          style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w900,
                              color: Colors.black.withOpacity(0.8)),
                        ),
                        const SizedBox(
                          height: 10,
                        ),
                        Text(
                          "チェックインを記録しました。",
                          style: TextStyle(
                              fontSize: 18,
                              fontWeight: FontWeight.w900,
                              color: Colors.black.withOpacity(0.8)),
                        ),
                      ],
                    ),
                    const SizedBox(
                      height: 60,
                    ),
                    PrimaryButton(
                      onTap: () {
                        Navigator.of(context).pushNamedAndRemoveUntil(
                          "/",
                          (_) => false,
                        );
                      },
                      text: "OK",
                      width: 140,
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  String _parseTimeDifference(double seconds) {
    final absSeconds = seconds.abs();

    final hour = absSeconds ~/ 3600;
    final minute = (absSeconds % 3600) ~/ 60;
    final second = absSeconds.toInt() % 60;

    String timeText = "";

    if (hour == 0 && minute == 0) {
      timeText = "$second秒";
    } else if (hour == 0) {
      timeText = "$minute分$second秒";
    } else {
      timeText = "$hour時間$minute分";
    }

    if (seconds < 0) {
      return "- $timeText";
    } else {
      return "+ $timeText";
    }
  }

  String _message(double seconds) {
    final now = DateTime.now();

    final sentences = [
      "いい朝ですね！",
      "今日も一日頑張っていきましょう！",
      "朝の時間を有効に使っていきましょう！",
    ];

    if (-120 < seconds && seconds < 0) {
      return "ギリギリセーフです！";
    } else if (now.hour < 7 && now.minute < 30) {
      return "とても早い朝ですね！";
    } else if (seconds < -3600) {
      return "余裕を持っていて素晴らしいです！";
    } else if (0 <= seconds && seconds < 300) {
      return "惜しい！ あともう少しでしたね！";
    } else if (0 < seconds) {
      return "寝坊してしまいましたか？";
    } else {
      final random = Random();
      return sentences[random.nextInt(sentences.length)];
    }
  }
}
