import 'package:flutter/material.dart';
import 'package:the_construct/services/constants.dart';
import 'package:the_construct/size_config/size_config.dart';

class Integration extends StatelessWidget {
  const Integration({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: SizeConfig.screenWidth,
      height: SizeConfig.screenWidth,
      child: Image.asset(launchScreen, fit: BoxFit.fill,),
    );
  }
}