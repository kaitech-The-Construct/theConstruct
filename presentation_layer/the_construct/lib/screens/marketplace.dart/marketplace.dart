import 'package:flutter/material.dart';
import 'package:the_construct/screens/marketplace.dart/components/navbar.dart';
import 'package:the_construct/size_config/size_config.dart';

import '../../services/constants.dart';
import '../search/search.dart';

class Marketplace extends StatelessWidget {
  const Marketplace({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.grey[300],
      child: const Column(
        children: [
          MarketplaceNavBar(),
          CustomSearchBar(),
        ],
      ),
    );
  }
}
