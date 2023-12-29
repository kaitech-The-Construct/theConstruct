import 'package:flutter/material.dart';
import 'package:the_construct/services/constants.dart';
import 'package:the_construct/size_config/size_config.dart';
import 'package:the_construct/ui/text_styles.dart';

import '../../search/search.dart';

class MarketplaceNavBar extends StatelessWidget {
  const MarketplaceNavBar({super.key});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: SizeConfig.screenHeight * .05,
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: List<Widget>.generate(
          navBarTitles.length,
          (index) => AppBarButton(title: navBarTitles[index], index: index),
        ),
      ),
    );
  }
}

class AppBarButton extends StatelessWidget {
  final String title;
  final int index;

  const AppBarButton({super.key, required this.title, required this.index});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 8.0),
      child: TextButton(
        onPressed: () {
          // Handle button tap here
        },
        child: Text(title, style: titleMedium(context)),
      ),
    );
  }
}
