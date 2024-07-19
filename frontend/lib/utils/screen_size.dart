import 'package:flutter/material.dart';

class ScreenSize {
  final BuildContext context;

  static late double width;
  static late double height;
  static late double topPadding;
  static late double bottomPadding;

  ScreenSize(this.context) {
    width = MediaQuery.of(context).size.width;
    height = MediaQuery.of(context).size.height;
    topPadding = MediaQuery.of(context).padding.top;
    bottomPadding = MediaQuery.of(context).padding.bottom;
  }
}
