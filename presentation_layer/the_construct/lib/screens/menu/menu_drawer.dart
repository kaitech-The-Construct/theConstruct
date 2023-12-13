import 'package:flutter/material.dart';
import 'package:the_construct/services/navigation/navigation.dart';
import 'package:the_construct/services/constants.dart';
import 'package:the_construct/size_config/size_config.dart';
import 'package:the_construct/ui/text_styles.dart';

// Menu Drawer
class MenuDrawer extends StatelessWidget {
  const MenuDrawer({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        FocusScope.of(context).requestFocus(FocusNode());
      },
      child: Drawer(
        child: Stack(
          children: [
            Positioned(
              child: Container(
                width: double.infinity, // Set width to cover the entire top
                height:
                    SizeConfig.screenWidth / 2.0, // Adjust the height as needed
                decoration: const BoxDecoration(
                  image: DecorationImage(
                    image: AssetImage(logo),
                    fit: BoxFit.cover, // Cover the entire area
                  ),
                ),
                child: null, // No need for an empty child here
              ),
            ),
            Positioned(
              top: SizeConfig.screenWidth / 2.5,
              child: SizedBox(
                width: SizeConfig.screenWidth,
                height: SizeConfig.screenHeight / 2,
                child: ListView(
                  children: <Widget>[
                    ListTile(
                      leading: const Icon(
                        Icons.home,
                        color: Color(0xFF123456),
                      ),
                      title: Text('Home', style: titleMedium(context)),
                      onTap: () {
                        router.pop();
                      },
                    ),
                    ListTile(
                      leading:
                          const Icon(Icons.build, color: Color(0xFF123456)),
                      title: Text('Marketplace', style: titleMedium(context)),
                      onTap: () async {
                        // Navigate to Robot Marketplace
                      },
                    ),
                    ListTile(
                      leading: const Icon(Icons.code_sharp,
                          color: Color(0xFF123456)),
                      title: Text('Software Repository',
                          style: titleMedium(context)),
                      onTap: () {
                        // Navigate to Software listings
                      },
                    ),
                    ListTile(
                      leading: const Icon(Icons.shopping_cart_sharp,
                          color: Color(0xFF123456)),
                      title: Text('Cart', style: titleMedium(context)),
                      onTap: () {
                        // Navigate to Software listings
                      },
                    ),
                    ListTile(
                      leading:
                          const Icon(Icons.person, color: Color(0xFF123456)),
                      title: Text('Profile', style: titleMedium(context)),
                      onTap: () {
                        router.pop();
                        router.goNamed('profile');
                      },
                    ),
                    ListTile(
                      leading: const Icon(Icons.support_agent_sharp,
                          color: Color(0xFF123456)),
                      title: Text('Support', style: titleMedium(context)),
                      onTap: () {
                        // Support agent on standby
                      },
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
