import 'package:flutter/material.dart';
import 'package:the_construct/screens/search/search.dart';

class Marketplace extends StatelessWidget {
  const Marketplace({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.grey[300],
      child: Column(children: [
        CustomSearchBar()
      ]),
    );
  }
}