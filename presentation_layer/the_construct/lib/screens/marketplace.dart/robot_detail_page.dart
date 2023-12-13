import 'package:flutter/material.dart';
import 'package:responsive_framework/responsive_framework.dart';
import 'package:the_construct/models/robot_catalog/robot_catalog_model.dart';
import 'package:the_construct/size_config/size_config.dart';
import 'package:the_construct/ui/text_styles.dart';

import '../../services/constants.dart';

class RobotDetailPage extends StatelessWidget {
  const RobotDetailPage({super.key, required this.details});

  final RobotDetails details;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        body: ResponsiveBreakpoints.of(context).largerThan(MOBILE)
            ? Row(
              
                children: [
                  Flexible(
                      child: SizedBox(
                    height: SizeConfig.screenHeight,
                    width: double.infinity,
                    child: Center(
                      child: Hero(
                        tag: details.model_id,
                        child: SizedBox(
                          width: SizeConfig.screenWidth * .3,
                          child: Card(
                            shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(25)),
                            elevation: 5,
                            child: ClipRRect(
                              borderRadius: const BorderRadius.all(
                                Radius.circular(25),
                              ),
                              child: Image.network(
                                details.image_url ?? softwareImage,
                                fit: BoxFit.cover,
                              ),
                            ),
                          ),
                        ),
                      ),
                    ),
                  )),
                  Flexible(
  child: SizedBox(
    height: SizeConfig.screenHeight,
    width: double.infinity,
    child: Container(
      color: Colors.green,
      child: Center(
        child: SizedBox(
          width: SizeConfig.screenWidth*.4,
          height: SizeConfig.screenHeight*.4,
          child: Card(
            shape: RoundedRectangleBorder(
                                borderRadius: BorderRadius.circular(25)),
                            elevation: 5,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisAlignment: MainAxisAlignment.center, // Center the content vertically
              children: [
                Padding(
                  padding: const EdgeInsets.only(left: 8.0),
                  child: Text(
                    details.manufacturer,
                    style: headlineSmall(context),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.only(left: 8.0),
                  child: Text(
                    details.model,
                    style: headlineMedium(context),
                  ),
                ),
                SizedBox(
                  height: SizeConfig.defaultPadding,
                ),
                Padding(
                  padding: const EdgeInsets.only(left: 8.0),
                  child: Text(
                    details.description,
                    style: titleMedium(context),
                  ),
                ),
                SizedBox(
                  height: SizeConfig.defaultPadding,
                ),
                Row(
              mainAxisAlignment: MainAxisAlignment.spaceAround,
              children: [
                InkWell(
                  child: Card(
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
                    elevation: 10,
                    color:  Colors.grey,
                    shadowColor:  Colors.grey,
                    child: SizedBox(
                      width: SizeConfig.screenWidth * .1,
                      height: SizeConfig.screenWidth * .05,
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            "Subscription",
                            style: titleMedium(context)
                                ?.copyWith(decoration: TextDecoration.underline),textAlign: TextAlign.center,
                          ),
                          Text(
                            details.price.subscription_price.toString(),
                            style: titleMedium(context),
                          )
                        ],
                      ),
                    ),
                  ),
                ),
                InkWell(
                  child: Card(
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
                    elevation: 10,
                    color:  Colors.grey,
                    shadowColor: const Color(0xFF115511),
                    child: SizedBox(
                      width: SizeConfig.screenWidth * .1,
                      height: SizeConfig.screenWidth * .05,
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            "Premium",
                            style: titleMedium(context)
                                ?.copyWith(decoration: TextDecoration.underline),textAlign: TextAlign.center,),
                          Text(
                            details.price.listing_price.toString(),
                            style: titleMedium(context),
                          )
                        ],
                      ),
                    ),
                  ),
                )
              ],
            )
              ],
            ),
          ),
        ),
      ),
    ),
  ),
)

                ],
              )
            : Column());
  }
}
      
      
//       Container(
//         color: Colors.white,
//         width: SizeConfig.screenWidth,
//         height: SizeConfig.screenHeight,
//         child: Column(
//           crossAxisAlignment: CrossAxisAlignment.start,
//           children: [
            // Hero(
            //   tag: details.model_id,
            //   child: SizedBox(
            //     width: double.infinity,
            //     height: SizeConfig.screenHeight * .5,
            //     child: Image.network(
            //       details.image_url ?? '',
            //       fit: BoxFit.fill,
            //     ),
            //   ),
            // ),
//             SizedBox(
//               height: SizeConfig.defaultPadding,
//             ),
//             Padding(
//               padding: const EdgeInsets.only(left: 8.0),
//               child: Text(
//                 details.manufacturer,
//                 style: headlineSmall(context),
//               ),
//             ),
//             Padding(
//               padding: const EdgeInsets.only(left: 8.0),
//               child: Text(
//                 details.model_id,
//                 style: titleLarge(context),
//               ),
//             ),
//             SizedBox(
//               height: SizeConfig.defaultPadding,
//             ),
//             Padding(
//               padding: const EdgeInsets.only(left: 8.0),
//               child: Text(
//                 details.description,
//                 style: titleMedium(context),
//               ),
//             ),
//             SizedBox(
//               height: SizeConfig.defaultPadding,
//             ),
//             Container(
//               color: Colors.grey,
//               height: 2,
//             ),
//             SizedBox(
//               height: SizeConfig.defaultPadding * 3,
//             ),
//             Row(
//               mainAxisAlignment: MainAxisAlignment.spaceAround,
//               children: [
//                 InkWell(
//                   child: Card(
//                     shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
//                     elevation: 10,
//                     color: const Color(0xFF115511),
//                     shadowColor: const Color(0xFF115511),
//                     child: SizedBox(
//                       width: SizeConfig.screenWidth * .4,
//                       height: SizeConfig.screenWidth * .25,
//                       child: Column(
//                         mainAxisAlignment: MainAxisAlignment.center,
//                         children: [
//                           Text(
//                             "Subscription",
//                             style: headlineSmall(context)
//                                 ?.copyWith(decoration: TextDecoration.underline),textAlign: TextAlign.center,
//                           ),
//                           Text(
//                             details.price.subscription_price.toString(),
//                             style: headlineSmall(context),
//                           )
//                         ],
//                       ),
//                     ),
//                   ),
//                 ),
//                 InkWell(
//                   child: Card(
//                     shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
//                     elevation: 10,
//                     color: const Color(0xFF115511),
//                     shadowColor: const Color(0xFF115511),
//                     child: SizedBox(
//                       width: SizeConfig.screenWidth * .4,
//                       height: SizeConfig.screenWidth * .25,
//                       child: Column(
//                         mainAxisAlignment: MainAxisAlignment.center,
//                         children: [
//                           Text(
//                             "Premium",
//                             style: headlineSmall(context)
//                                 ?.copyWith(decoration: TextDecoration.underline),textAlign: TextAlign.center,),
//                           Text(
//                             details.price.listing_price.toString(),
//                             style: headlineSmall(context),
//                           )
//                         ],
//                       ),
//                     ),
//                   ),
//                 )
//               ],
//             )
//           ],
//         ),
//       ),
//     );
//   }
// }
