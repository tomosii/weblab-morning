import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';

import 'dialog_button.dart';

class MorningErrorDialog extends StatelessWidget {
  final String title;
  final String message;
  final String? buttonText;

  const MorningErrorDialog({
    Key? key,
    required this.title,
    required this.message,
    this.buttonText,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Dialog(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15),
      ),
      child: Container(
        constraints: const BoxConstraints(
          maxWidth: 500,
        ),
        padding: const EdgeInsets.only(
          left: 27,
          right: 20,
          top: 25,
          bottom: 30,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Row(
              children: [
                // Lottie.asset(
                //   "assets/lottie/error_alert.json",
                //   width: 36,
                // ),
                // const SizedBox(
                //   width: 5,
                // ),
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 16,
                    color: Colors.black.withOpacity(0.75),
                    fontWeight: FontWeight.w800,
                    height: 1.2,
                  ),
                ),
              ],
            ),
            const SizedBox(
              height: 8,
            ),
            Padding(
              padding: const EdgeInsets.only(left: 0),
              child: Text(
                message,
                textAlign: TextAlign.left,
                style: TextStyle(
                  fontSize: 13,
                  color: Colors.black.withOpacity(0.5),
                  fontWeight: FontWeight.w500,
                  height: 1.7,
                ),
              ),
            ),
            const SizedBox(
              height: 35,
            ),
            Center(
              child: QwiDialogButton(
                width: 100,
                height: 40,
                onTap: () {
                  Navigator.of(context).pop();
                },

                // backgroundColor: Colors.grey[200]!,
                // foregroundColor: Colors.grey[600]!,
                text: "閉じる",
              ),
            ),
          ],
        ),
      ),
    );
  }
}
