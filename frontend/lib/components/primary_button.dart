// プライマリーボタン（文字が白）
import 'package:flutter/material.dart';
import 'package:morning_web/constants/colors.dart';

class PrimaryButton extends StatelessWidget {
  final String text;
  final IconData? icon;
  final Function() onTap;
  final double width;
  final bool loading;

  const PrimaryButton({
    Key? key,
    this.text = "",
    this.icon,
    required this.onTap,
    this.width = double.infinity,
    this.loading = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 50,
      width: width,
      child: ElevatedButton(
        onPressed: onTap,
        style: ElevatedButton.styleFrom(
          backgroundColor: morningBgBlue,
          foregroundColor: morningFgBlue,
          shape: const StadiumBorder(),
          shadowColor: Colors.transparent,
        ),
        child: _buttonChild(),
      ),
    );
  }

  Widget _buttonChild() {
    if (loading) {
      return SizedBox(
        width: 20,
        height: 20,
        child: CircularProgressIndicator(
          strokeWidth: 2.5,
          color: morningFgBlue,
        ),
      );
    } else if (icon != null) {
      return Icon(
        icon,
        color: morningFgBlue,
        size: 25,
      );
    } else {
      return Text(
        text,
        style: TextStyle(
          fontSize: 15,
          fontWeight: FontWeight.bold,
          color: morningFgBlue,
        ),
      );
    }
  }
}
