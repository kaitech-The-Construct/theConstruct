import 'package:flutter/material.dart';
import 'package:the_construct/services/project_initializer.dart';

import 'services/navigation/navigation.dart';
import 'size_config/size_config.dart';
import 'ui/responsive.dart';
import 'ui/theme.dart';

void main() async{
  await projectInitializer();
  runApp(const TheConstructApp());
}

class TheConstructApp extends StatelessWidget {
  const TheConstructApp({super.key});

  @override
  Widget build(BuildContext context) {
    SizeConfig().init(context);
    return MaterialApp.router(
      builder: (_, widget) => responsiveWrapperBuilder(context, widget!),
      theme: appThemeData,
      routerConfig: router,
    
      debugShowCheckedModeBanner: false,
    );
  }
}


