import 'package:flutter/material.dart';
import 'package:the_construct/services/constants.dart';
import 'package:the_construct/size_config/size_config.dart';
import 'package:the_construct/ui/text_styles.dart';
import 'package:url_launcher/url_launcher.dart';

import '../home/components/snackbar.dart';

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
            SizedBox(
              // color: Colors.grey,
              height: SizeConfig.screenHeight,
              child: Column(children: [
                Container(
                  width: double.infinity, // Set width to cover the entire top
                  height: SizeConfig.screenHeight *
                      .3, // Adjust the height as needed
                  decoration: const BoxDecoration(
                    image: DecorationImage(
                      image: AssetImage(logo),
                      fit: BoxFit.cover, // Cover the entire area
                    ),
                  ),
                  child: null, // No need for an empty child here
                ),
                ListTile(
                    leading: const Icon(
                      Icons.home,
                      color: Color(0xFF123456),
                    ),
                    title: Text('Home', style: titleMedium(context)),
                    onTap: () {
                      comingSoonSnackbar(context);
                    }),
                ListTile(
                  leading: const Icon(Icons.build, color: Color(0xFF123456)),
                  title: Text('Marketplace', style: titleMedium(context)),
                  onTap: () async {
                    launchUrl(
                                      Uri.parse(
                                          'https://injective-service-bu6vz2kbtq-uc.a.run.app'),
                                      mode: LaunchMode.externalApplication);
                  },
                ),
                ListTile(
                  leading: const Icon(Icons.shopping_cart_sharp,
                      color: Color(0xFF123456)),
                  title: Text('Cart', style: titleMedium(context)),
                  onTap: () {
                    // Navigate to Software listings

                    comingSoonSnackbar(context);
                  },
                ),
                ListTile(
                    leading:
                        const Icon(Icons.inventory, color: Color(0xFF123456)),
                    title: Text('Inventory', style: titleMedium(context)),
                    onTap: () {
                      // router.goNamed('profile');

                      comingSoonSnackbar(context);
                    }),
                ListTile(
                  leading: const Icon(Icons.support_agent_sharp,
                      color: Color(0xFF123456)),
                  title: Text('Support', style: titleMedium(context)),
                  onTap: () {
                    // Support agent on standby

                    comingSoonSnackbar(context);
                  },
                ),
                ListTile(
                  leading: const Icon(Icons.precision_manufacturing,
                      color: Color(0xFF123456)),
                  title: Text('Manufacturers', style: titleMedium(context)),
                  onTap: () {
                    // router.goNamed('profile');

                    comingSoonSnackbar(context);
                  },
                ),
                ListTile(
                  leading:
                      const Icon(Icons.code_sharp, color: Color(0xFF123456)),
                  title:
                      Text('Software Developers', style: titleMedium(context)),
                  onTap: () {
                    // router.goNamed('profile');

                    comingSoonSnackbar(context);
                  },
                ),
              ]),
            ),
          ],
        ),
      ),
    );
  }
}
