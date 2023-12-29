import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';
import 'package:the_construct/models/robot_catalog/robot_catalog_model.dart';
import 'package:the_construct/screens/landing_page/landing_page.dart';
import 'package:the_construct/screens/marketplace.dart/marketplace.dart';
import 'package:the_construct/screens/marketplace.dart/robot_detail_page.dart';

import '../../bloc/generics/generic_bloc.dart';
import '../../repositories/robot_repository.dart';
import '../../screens/home/home.dart';
import '../../screens/user_profile.dart/profile.dart';
import '../widgets/loading.dart';

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
      GoRoute(
        name: 'marketplace',
        path: '/marketplace',
        builder: (BuildContext context, GoRouterState state) {
          return FutureBuilder(
              future: Future.delayed(const Duration(milliseconds: 30)),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Loading();
                } else {
                  return BlocProvider<
                          GenericBloc<RobotDetails, RobotDetailsRepository>>(
                      create: (BuildContext context) =>
                          GenericBloc<RobotDetails, RobotDetailsRepository>(
                              repository: RobotDetailsRepository()),
                      child: const Marketplace());
                }
              });
        },
      ),
      GoRoute(
        name: 'robotDetails',
        path: '/robotDetails/:model_id',
        builder: (BuildContext context, GoRouterState state) {
          RobotDetails details = state.extra as RobotDetails;
          return RobotDetailPage(
            details: details,
          );
        },
      ),
      // GoRoute(
      //   name: 'taskDetail',
      //   path: 'taskDetail/:task_id', // Define a dynamic parameter
      //   builder: (BuildContext context, GoRouterState state) {
      //     if (state.extra == null) {
      //       router.go('/');
      //       return Container();
      //     } else {
      //       TaskModel task = state.extra as TaskModel;
      //       return DetailedTaskScreen(task: task);
      //     }
      //   },
      // ),
    ],
  )
]);
