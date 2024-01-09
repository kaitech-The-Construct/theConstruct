import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:the_construct/screens/landing_page/landing_page.dart';

import '../../screens/home/home.dart';
import '../../screens/user_profile.dart/profile.dart';

final GlobalKey<NavigatorState> _rootNavigatorKey = GlobalKey<NavigatorState>();

final GlobalKey<NavigatorState> _shellNavigatorKey =
    GlobalKey<NavigatorState>();

///Go router navigation
final GoRouter router =
    GoRouter(navigatorKey: _rootNavigatorKey, initialLocation: '/', routes: [
  ShellRoute(
    navigatorKey: _shellNavigatorKey,
    builder: (context, state, child) => HomePage(pageWidget: child),
    routes: [
      GoRoute(
        path: '/',
        name: 'home',
        builder: (BuildContext context, GoRouterState state) {
          return const LandingPageWidget();
        },
      ),
      GoRoute(
        name: 'profile',
        path: '/profile',
        builder: (BuildContext context, GoRouterState state) {
          return const ProfilePage();
        },
      ),
    ],
  ),
]);

