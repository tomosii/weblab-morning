import 'package:flutter/material.dart';

import '../../constants/colors.dart';

class QwiDialogButton extends StatelessWidget {
  const QwiDialogButton({
    Key? key,
    this.width,
    this.height,
    this.backgroundColor = morningBgBlue,
    this.foregroundColor = morningFgBlue,
    this.text,
    this.onTap,
  }) : super(key: key);

  final double? width;
  final double? height;
  final Color backgroundColor;
  final Color foregroundColor;
  final String? text;
  final Function()? onTap;

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: width ?? double.infinity,
      height: height ?? 45,
      child: ElevatedButton(
        onPressed: onTap,
        style: ElevatedButton.styleFrom(
          elevation: 0,
          backgroundColor: backgroundColor,
          foregroundColor: foregroundColor,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(8),
          ),
          padding: const EdgeInsets.symmetric(vertical: 10),
        ),
        child: Text(
          text ?? "",
          style: const TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.w700,
          ),
        ),
      ),
    );
  }
}
