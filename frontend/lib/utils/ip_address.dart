import 'dart:convert';

import 'package:http/http.dart' as http;

Future<String> getIPAddress() async {
  final response =
      await http.get(Uri.parse('https://api.ipify.org?format=json'));
  if (response.statusCode == 200) {
    final ipAddress = jsonDecode(response.body)['ip'];
    print("Current IP address: $ipAddress");
    return ipAddress;
  } else {
    throw Exception('Failed to get IP address');
  }
}
