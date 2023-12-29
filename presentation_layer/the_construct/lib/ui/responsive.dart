import 'package:flutter/material.dart';
import 'package:responsive_framework/responsive_framework.dart';

///Responsive wrapper
Widget responsiveWrapperBuilder(BuildContext context, Widget widget) {
  return ResponsiveBreakpoints.builder(
    child: widget,
    breakpoints: <Breakpoint>[
      const Breakpoint(start: 0, end: 450, name: MOBILE),
      const Breakpoint(start: 451, end: 1150, name: TABLET),
      const Breakpoint(start: 1151, end: double.infinity, name: DESKTOP),
    ],
  );
}

bool isDesktop(BuildContext context) =>
    ResponsiveBreakpoints.of(context).isDesktop;
bool isTablet(BuildContext context) =>
    ResponsiveBreakpoints.of(context).isTablet;
bool isMobile(BuildContext context) =>
    ResponsiveBreakpoints.of(context).isMobile;
