import 'package:flutter/material.dart';

import '../constants.dart';

Widget imageWidget(String? url) {
  return Card(
    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
    elevation: 5,
    child: ClipRRect(
      borderRadius: const BorderRadius.all(
        Radius.circular(25),
      ),
      child: Image.network(
        url ?? softwareImage,
        fit: BoxFit.cover,
      ),
    ),
  );
}
