import 'package:flutter/material.dart';
import 'package:the_construct/screens/landing_page/landing_page_features.dart';
import 'package:the_construct/services/constants.dart';
import 'package:the_construct/services/widgets/image_widget.dart';
import 'package:the_construct/size_config/size_config.dart';

import '../../models/robot_catalog/robot_catalog_model.dart';
import '../../models/software_repo/software_repository_model.dart';
import '../../services/api/api_functions.dart';
import '../../ui/text_styles.dart';
import '../home/components/featured.dart';

class LandingPageWidget extends StatelessWidget {
  const LandingPageWidget({
    super.key,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: SizeConfig.screenHeight,
      width: SizeConfig.screenWidth,
      child: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            const SizedBox(height: 20),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                children: [
                  Flexible(
                    child: Column(
                      
                      children: [
                        Padding(
                          padding:
                              const EdgeInsets.only(right: 16.0, bottom: 16.0),
                          child: Text(
                            tagline,
                            style: headlineMedium(context)
                                ?.copyWith(color: const Color(0xFF115511)),
                          ),
                        ),
                        Padding(
                          padding:
                              const EdgeInsets.only(right: 16.0, bottom: 16.0),
                          child: Text(
                            overview,
                            style: titleMedium(context)
                                ?.copyWith(color: const Color(0xFF115511)),
                          ),
                        ),
                      ],
                    ),
                  ),
                  Flexible(
                    
                    child: imageWidget(landing_1),
                  )
                ],
              ),
            ),
            const SizedBox(height: 30),
            const LandingPageFeatures(),
            const SizedBox(height: 20),
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Text(featured,style: headlineLarge(context)?.copyWith(color: const Color(0xFF115511)),),
            ),
            // Featured Robots and Software Widget
            FutureBuilder<List<RobotDetails>>(
                future: APIFunctions().getRobotList(),
                builder: (context, snapshot) {
                  if (snapshot.hasData) {
                    List<RobotDetails> robotList =
                        snapshot.data as List<RobotDetails>;
                    return FeaturedRobots(
                  title: "Robots",
                      items: robotList.sublist(1, 4),
                    );
                  }
                  return const FeaturedRobots(
                 title: "Robots",
                    items: [],
                  );
                }),
            const SizedBox(height: 30),
            // FutureBuilder<List<SoftwareDetails>>(
            //     future: APIFunctions().getSoftwareList(),
            //     builder: (context, snapshot) {
            //       if (snapshot.hasData) {
            //         List<SoftwareDetails> softwareList =
            //             snapshot.data as List<SoftwareDetails>;
            //         return FeaturedSoftware(
            //           title: 'Latest Software',
            //           items: softwareList.sublist(0, 3),
            //         );
            //       }
            //       return const FeaturedSoftware(
            //         title: 'Latest Software',
            //         items: [],
            //       );
            //     }),
          ],
        ),
      ),
    );
  }
}
