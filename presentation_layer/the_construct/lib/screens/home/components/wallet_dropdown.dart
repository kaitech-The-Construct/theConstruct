import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:the_construct/services/constants.dart';
import 'package:the_construct/ui/text_styles.dart';

import '../../../services/api/wallet_connect.dart';

class WalletDropdownButton extends StatefulWidget {
  const WalletDropdownButton({Key? key});

  @override
  WalletDropdownButtonState createState() => WalletDropdownButtonState();
}

class WalletDropdownButtonState extends State<WalletDropdownButton> {
  String selectedOption = 'Select Wallet'; // Default selection

  @override
  Widget build(BuildContext context) {
    return DropdownButton<String>(
      underline: const SizedBox(height: 0,),
      focusColor: Colors.white,
      dropdownColor: Colors.white,
      value: selectedOption,
      icon: const Icon(Icons.person_sharp),
      iconSize: 28,
      style: titleLarge(context),
      onChanged: (value) {
        setState(() {
          selectedOption = value ?? walletOptions.first;
          if (selectedOption == 'Keplr') {
            getKeplrAddress().then((String? address) {
              if (address != null) {
                // Handle the Keplr address here
                if (kDebugMode) {
                  print('Keplr Address: $address');
                }
              } else {
                if (kDebugMode) {
                  print('Keplr Address not found');
                }
                selectedOption = walletOptions.first;
              }
            });
          } else if (selectedOption == 'Metamask') {
            selectedOption = value ?? walletOptions.first;
            getEthAddressFromMetaMask().then((String? address) {
              if (address != null) {
                // Handle the MetaMask address here
                if (kDebugMode) {
                  print('MetaMask Address: $address');
                }
              } else {
                if (kDebugMode) {
                  print('MetaMask Address not found');
                }
                selectedOption = walletOptions.first;
              }
            });
          }
        });
      },
      items: walletOptions.map<DropdownMenuItem<String>>((String value) {
        return DropdownMenuItem<String>(
          value: value,
          child: OptionCard(optionText: value),
        );
      }).toList(),
    );
  }
}

class OptionCard extends StatelessWidget {
  final String optionText;

  const OptionCard({super.key, required this.optionText});

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12.0),
      ),
      elevation: 4,
      child: Padding(
        padding: const EdgeInsets.all(8.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Icon(
              Icons.account_balance_wallet,
              size: 24,
              color: Colors.deepPurple,
            ),
            const SizedBox(width: 16),
            Text(
              optionText,
              style: const TextStyle(
                fontSize: 20,
                color: Colors.deepPurple,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
