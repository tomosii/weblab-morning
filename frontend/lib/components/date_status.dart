import 'package:flutter/material.dart';
import 'package:morning_web/utils/date.dart';

import '../constants/colors.dart';
import '../models/date_status.dart';

class DateStatusIndicator extends StatelessWidget {
  final DateStatus status;

  const DateStatusIndicator({
    super.key,
    required this.status,
  });

  Color get bgColor {
    if (!status.commitEnabled || !status.isWeekday) {
      return Colors.black.withOpacity(0.05);
    } else if (status.point == null) {
      return morningBgBlue;
    } else if (status.point! > 0) {
      return morningBlue;
    } else {
      return morningPink;
    }
  }

  Color get textColor {
    if (!status.commitEnabled || !status.isWeekday) {
      return Colors.black.withOpacity(0.2);
    } else if (status.point == null) {
      return morningFgBlue;
    } else {
      return Colors.white;
    }
  }

  Widget get child {
    if (!status.commitEnabled || !status.isWeekday) {
      return Container();
    } else if (status.point == null) {
      return Container(
        padding: const EdgeInsets.only(
          top: 5,
          bottom: 3,
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              getJPDayOfWeekString(status.date.weekday),
              style: TextStyle(
                fontSize: 10,
                fontWeight: FontWeight.w400,
                color: textColor.withOpacity(0.5),
                height: 1.0,
              ),
            ),
            const SizedBox(
              height: 5,
            ),
            Text(
              status.date.day.toString(),
              style: TextStyle(
                fontFamily: "Inter",
                fontSize: 21,
                fontWeight: FontWeight.w500,
                color: textColor,
                height: 1.0,
              ),
            ),
          ],
        ),
      );
    } else if (status.point! > 0) {
      return const Center(
          child: Icon(
        Icons.check_rounded,
        color: Colors.white,
        size: 27,
      ));
    } else {
      return Center(
        child: Text(
          status.point.toString(),
          style: TextStyle(
            fontFamily: "Inter",
            fontSize: 21,
            fontWeight: FontWeight.w500,
            color: textColor,
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 52,
      height: 52,
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(7),
      ),
      child: child,
    );
  }
}
