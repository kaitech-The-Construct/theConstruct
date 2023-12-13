import 'package:flutter/material.dart';

import '../../services/navigation/navigation.dart';
import '../../services/constants.dart';
import '../../size_config/size_config.dart';
import '../../ui/text_styles.dart';
import 'components/wallet_dropdown.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key, required this.pageWidget});
  final Widget pageWidget;
  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  int selectedTileIndex = 0; // Index of the selected ListTile

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SizedBox(
          height: SizeConfig.screenHeight,
          width: SizeConfig.screenWidth,
          child: SingleChildScrollView(
            child: Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Flexible(
                  flex: 1,
                  child: SizedBox(
                    // color: Colors.grey,
                    height: SizeConfig.screenHeight,
                    child: Column(children: [
                      Container(
                        width: double
                            .infinity, // Set width to cover the entire top
                        height: SizeConfig.screenHeight *
                            .2, // Adjust the height as needed
                        decoration: const BoxDecoration(
                          image: DecorationImage(
                            image: AssetImage(logo),
                            fit: BoxFit.cover, // Cover the entire area
                          ),
                        ),
                        child: null, // No need for an empty child here
                      ),
                      ListTile(
                        selected: selectedTileIndex == 0,
                        selectedTileColor: Colors.grey,
                        leading: const Icon(
                          Icons.home,
                          color: Color(0xFF123456),
                        ),
                        title: Text('Home', style: titleMedium(context)),
                        onTap: () {
                          router.goNamed('home');
                          setState(() {
                            selectedTileIndex = 0;
                          });
                        },
                      ),
                      ListTile(
                        selected: selectedTileIndex == 1,
                        selectedTileColor: Colors.grey,
                        leading:
                            const Icon(Icons.build, color: Color(0xFF123456)),
                        title: Text('Marketplace', style: titleMedium(context)),
                        onTap: () async {
                          // Navigate to Robot Marketplace
                          router.goNamed('marketplace');
                          setState(() {
                            selectedTileIndex = 1;
                          });
                        },
                      ),
                    
                      ListTile(
                        selected: selectedTileIndex == 2,
                        selectedTileColor: Colors.grey,
                        leading: const Icon(Icons.shopping_cart_sharp,
                            color: Color(0xFF123456)),
                        title: Text('Cart', style: titleMedium(context)),
                        onTap: () {
                          // Navigate to Software listings
                          setState(() {
                            selectedTileIndex = 2;
                          });
                        },
                      ),
                      ListTile(
                        selected: selectedTileIndex == 3,
                        selectedTileColor: Colors.grey,
                        leading: const Icon(Icons.inventory,
                            color: Color(0xFF123456)),
                        title: Text('Inventory', style: titleMedium(context)),
                        onTap: () {
                          router.goNamed('profile');
                          setState(() {
                            selectedTileIndex = 3;
                          });
                        },
                      ),
                      ListTile(
                        selected: selectedTileIndex == 4,
                        selectedTileColor: Colors.grey,
                        leading: const Icon(Icons.support_agent_sharp,
                            color: Color(0xFF123456)),
                        title: Text('Support', style: titleMedium(context)),
                        onTap: () {
                          // Support agent on standby
                          setState(() {
                            selectedTileIndex = 4;
                          });
                        },
                      ),
                       ListTile(
                        selected: selectedTileIndex == 5,
                        selectedTileColor: Colors.grey,
                        leading: const Icon(Icons.precision_manufacturing,
                            color: Color(0xFF123456)),
                        title: Text('Manufacturers', style: titleMedium(context)),
                        onTap: () {
                          router.goNamed('profile');
                          setState(() {
                            selectedTileIndex = 5;
                          });
                        },
                      ),
                       ListTile(
                        selected: selectedTileIndex == 6,
                        selectedTileColor: Colors.grey,
                        leading: const Icon(Icons.code_sharp,
                            color: Color(0xFF123456)),
                        title: Text('Software Developers', style: titleMedium(context)),
                        onTap: () {
                          router.goNamed('profile');
                          setState(() {
                            selectedTileIndex = 6;
                          });
                        },
                      ),
                      
                    ]),
                  ),
                ),
                Flexible(
                    flex: 4,
                    child: SizedBox(
                        height: SizeConfig.screenHeight,
                        width: SizeConfig.screenWidth,
                        child: Column(
                          children: [
                            Align(
                              alignment: Alignment.centerRight,
                              child: Padding(
                                  padding:
                                      const EdgeInsets.only(top: 8, right: 16),
                                  child: WalletDropdownButton()),
                            ),
                           Expanded(child:  widget.pageWidget,)
                          ],
                        ))),
              ],
            ),
          )),
    );
  }
}
