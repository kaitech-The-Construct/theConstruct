import 'package:flutter/material.dart';
import 'package:the_construct/models/robot_catalog/robot_catalog_model.dart';
import 'package:the_construct/models/software_repo/software_repository_model.dart';
import 'package:the_construct/size_config/size_config.dart';
import 'package:the_construct/ui/text_styles.dart';

import '../../../services/constants.dart';

class FeaturedRobots extends StatelessWidget {
  final String title;
  final List<RobotDetails> items;

  const FeaturedRobots({
    Key? key,
    required this.title,
    required this.items,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0),
          child: Text(
            title,
            style: headlineSmall(context),
          ),
        ),
        SizedBox(
          height: 250,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: items.length,
            itemBuilder: (context, index) {
              RobotDetails item = items[index];
              return Hero(
                tag: item.model_id,
                child: Padding(
                  padding: const EdgeInsets.only(left: 8.0, right: 8.0),
                  child: SizedBox(
                    width: SizeConfig.screenWidth * .25,
                    height: SizeConfig.screenHeight * .3,
                    child: Card(
                          shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(25)),
                          elevation: 5,
                          child: ClipRRect(
                            borderRadius: const BorderRadius.all(
                              Radius.circular(25),
                            ),
                            child: Image.network(
                              item.image_url ?? softwareImage,
                              fit: BoxFit.cover,
                            ),
                          ),
                        ),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}

class FeaturedSoftware extends StatelessWidget {
  final String title;
  final List<SoftwareDetails> items;

  const FeaturedSoftware({
    Key? key,
    required this.title,
    required this.items,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16.0),
          child: Text(
            title,
            style: headlineSmall(context),
          ),
        ),
        SizedBox(
          height: 250,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: items.length,
            itemBuilder: (context, index) {
              SoftwareDetails item = items[index];
              return Padding(
                padding: const EdgeInsets.only(left: 8.0, right: 8.0),
                child: SizedBox(
                  width: SizeConfig.screenWidth * .25,
                  height: SizeConfig.screenHeight * .3,
                  child: Card(
                            shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(25)),
                            elevation: 5,
                            child: ClipRRect(
                              borderRadius: const BorderRadius.all(
                                Radius.circular(25),
                              ),
                              child: Image.network(
                                item.image_url ?? softwareImage,
                                fit: BoxFit.cover,
                              ),
                            ),
                          ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }
}
