import 'package:flutter/material.dart';
import 'package:the_construct/ui/text_styles.dart';

ScaffoldFeatureController<SnackBar, SnackBarClosedReason> comingSoonSnackbar(
    BuildContext context) {
  return ScaffoldMessenger.of(context).showSnackBar( SnackBar(
    content: Center(
      child: Text(
        'New Features Coming Soon!',
        style:titleMedium(context)?.copyWith(color: Colors.white)
      ),
    ),
    backgroundColor:  const Color(0xFF115511), 
    behavior: SnackBarBehavior.floating,
    duration: const Duration(seconds: 2), 
  ));
}
