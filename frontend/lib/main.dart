import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_web_plugins/url_strategy.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

import 'constants/colors.dart';
import 'firebase_options.dart';
import 'pages/email_page.dart';
import 'pages/home_page.dart';
import 'pages/loading_page.dart';
import 'pages/result_page.dart';
import 'providers/providers.dart';
import 'utils/screen_size.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  print("Loading Firebase...");
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  usePathUrlStrategy();
  print("Loading .env file...");
  await dotenv.load(fileName: "env");

  runApp(
    ProviderScope(
      child: MaterialApp(
        locale: const Locale("ja", "JP"),
        title: "朝活",
        theme: ThemeData(
          primarySwatch: Colors.blue,
          fontFamily: "NotoSansJP",
          useMaterial3: false,
        ),
        scrollBehavior: const MaterialScrollBehavior().copyWith(
          dragDevices: {
            PointerDeviceKind.touch,
            PointerDeviceKind.mouse,
          },
        ),
        home: const MorningApp(),
        routes: {
          "/result": (_) => const CheckInResultPage(),
          "/loading": (_) => const CheckInLoadingPage(),
        },
      ),
    ),
  );
}

class MorningApp extends ConsumerStatefulWidget {
  const MorningApp({super.key});

  @override
  ConsumerState<MorningApp> createState() => _MorningAppState();
}

class _MorningAppState extends ConsumerState<MorningApp> {
  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    ScreenSize(context);
    ref.invalidate(localEmailProvider);
  }

  @override
  Widget build(BuildContext context) {
    return ref.watch(localEmailProvider).when(
          data: (email) {
            if (email != null) {
              return const HomePage();
            } else {
              return const EmailPage();
            }
          },
          loading: () => const Scaffold(
            body: Center(
              child: CircularProgressIndicator(
                color: morningBlue,
              ),
            ),
          ),
          error: (error, stackTrace) {
            return Center(
              child: Text(
                "エラー: ${error.toString()}",
                style: const TextStyle(
                  fontSize: 13,
                  color: Colors.black38,
                ),
              ),
            );
          },
        );
  }
}
