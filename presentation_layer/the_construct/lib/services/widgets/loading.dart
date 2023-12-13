import 'package:flutter/material.dart';
import 'package:flutter_spinkit/flutter_spinkit.dart';

import '../../size_config/size_config.dart';

class Loading extends StatelessWidget{
  const Loading({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: SizeConfig.screenHeight,
      width: SizeConfig.screenWidth,
      color: Colors.white,
      child:  Center(
        child: SpinKitChasingDots(
          color: Colors.green[900],
          duration: const Duration(seconds: 5),
        ),
      ),
    );
  }
}
