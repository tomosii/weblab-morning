import 'package:flutter/material.dart';

import '../constants/colors.dart';

class SimpleTextForm extends StatefulWidget {
  const SimpleTextForm({
    Key? key,
    required this.hintText,
    required this.controller,
    required this.node,
    this.password = false,
    this.done = false,
    this.autofillHint,
    this.onChanged,
  }) : super(key: key);

  final String hintText;
  final TextEditingController controller;
  final FocusScopeNode node;
  final bool password;
  final bool done;
  final String? autofillHint;
  final void Function(String)? onChanged;

  @override
  State<SimpleTextForm> createState() => _SimpleTextFormState();
}

class _SimpleTextFormState extends State<SimpleTextForm> {
  static final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 60,
      padding: const EdgeInsets.symmetric(horizontal: 20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(10),
        boxShadow: [
          BoxShadow(
            color: Colors.blueGrey.withOpacity(0.1),
            spreadRadius: 2,
            blurRadius: 18,
            offset: const Offset(0, 2),
          ),
        ],
        border: Border.all(
          color: Colors.black.withOpacity(0.12),
          width: 0.5,
        ),
      ),
      child: Align(
        alignment: Alignment.center,
        child: TextField(
          key: _formKey,
          autocorrect: false,
          autofillHints:
              (widget.autofillHint != null) ? [widget.autofillHint!] : null,
          controller: widget.controller,
          onChanged: widget.onChanged,
          cursorHeight: 23,
          cursorColor: morningBlue,
          enableInteractiveSelection: false,
          obscureText: widget.password,
          textInputAction:
              widget.done ? TextInputAction.done : TextInputAction.next,
          onEditingComplete: () =>
              widget.done ? widget.node.unfocus() : widget.node.nextFocus(),
          style: TextStyle(
            color: Colors.grey[800],
            fontWeight: FontWeight.w500,
            fontSize: 15,
          ),
          decoration: InputDecoration(
            hintText: widget.hintText,
            hintStyle: TextStyle(
              color: Colors.black.withOpacity(0.3),
              fontWeight: FontWeight.w500,
              fontSize: 13,
            ),
            border: InputBorder.none,
            counterText: "",
          ),
        ),
      ),
    );
  }
}

// Widget oneLineTextField(
//     String hintText, TextEditingController _controller, FocusScopeNode node,
//     {bool password = false,
//     bool done = false,
//     void Function(String)? onChanged}) {
//   return Container(
//     // width: ScreenSize.width * 0.75,
//     height: 55,
//     padding: const EdgeInsets.symmetric(horizontal: 20),
//     decoration: BoxDecoration(
//       color: Colors.white,
//       borderRadius: BorderRadius.circular(15),
//       // border: Border.all(color: (Colors.grey[200])!),
//       // ignore: prefer_const_literals_to_create_immutables
//       boxShadow: [
//         const BoxShadow(
//           color: Colors.black12,
//           spreadRadius: 2,
//           blurRadius: 6,
//           offset: Offset(0, 2),
//         ),
//       ],
//     ),
//     child: Align(
//       alignment: Alignment.center,
//       child: TextField(
//         controller: _controller,
//         onChanged: onChanged,
//         cursorHeight: 23,
//         cursorColor: qwiGreen,
//         enableInteractiveSelection: false,
//         obscureText: password,
//         textInputAction: done ? TextInputAction.done : TextInputAction.next,
//         onEditingComplete: () => done ? node.unfocus() : node.nextFocus(),
//         style: TextStyle(
//           color: Colors.grey[800],
//           fontSize: 16,
//         ),
//         decoration: InputDecoration(
//           hintText: hintText,
//           hintStyle: TextStyle(
//             color: Colors.black.withOpacity(0.3),
//             fontSize: 13,
//           ),
//           border: InputBorder.none,
//           counterText: "",
//         ),
//       ),
//     ),
//   );
// }
