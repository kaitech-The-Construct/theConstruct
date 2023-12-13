import 'package:flutter/material.dart';
import 'package:flutter_staggered_grid_view/flutter_staggered_grid_view.dart';
import 'package:the_construct/services/constants.dart';
import 'package:the_construct/size_config/size_config.dart';
import 'package:the_construct/ui/text_styles.dart';

class LandingPageFeatures extends StatelessWidget {
  const LandingPageFeatures({Key? key});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(16.0),
      child: Row(
        children: [
          Flexible(child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Text(features,style: headlineLarge(context)?.copyWith(color: const Color(0xFF115511),)),
            ),),
          Flexible(
            flex: 3,
            child: SizedBox(
                height: SizeConfig.screenHeight*.8,
                child: GridView.custom(
                  gridDelegate: SliverWovenGridDelegate.count(
                    crossAxisCount: 2,
                    mainAxisSpacing: 6,
                    crossAxisSpacing: 6,
                    pattern: [
                      const WovenGridTile(1),
                      const WovenGridTile(
                        5 / 4,
                        crossAxisRatio: 1,
                        alignment: AlignmentDirectional.centerEnd,
                      ),
                    ],
                  ),
                  childrenDelegate: SliverChildBuilderDelegate(
                      (context, index) => CardWidget(index),
                      childCount: 4),
                  physics: const NeverScrollableScrollPhysics(),
                )),
          ),
        ],
      ),
    );
  }
}

class CardWidget extends StatelessWidget {
  final int index;

  CardWidget(this.index);

  @override
  Widget build(BuildContext context) {
    LandingPageData data = landingPageData[index];
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Card(
        elevation: 4.0,
       shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(25)),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                data.title,
                style: headlineMedium(context)?.copyWith(color: const Color(0xFF115511)),
              ),
              const SizedBox(height:20),
              Text(data.text, style: titleMedium(context)?.copyWith(height: 1.75),),
              
            ],
          ),
        ),
      ),
    );
  }
}
