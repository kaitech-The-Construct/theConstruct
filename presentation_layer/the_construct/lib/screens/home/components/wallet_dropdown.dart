import 'package:flutter/material.dart';
import 'package:nil/nil.dart';
import 'package:the_construct/services/constants.dart';
import 'package:the_construct/ui/text_styles.dart';

class WalletDropdownButton extends StatefulWidget {
  @override
  WalletDropdownButtonState createState() => WalletDropdownButtonState();
}

class WalletDropdownButtonState extends State<WalletDropdownButton> {
  String selectedOption = 'Select Wallet'; // Default selection

  @override
  Widget build(BuildContext context) {
    return DropdownButton<String>(
      underline: nil,
      focusColor: Colors.white,
      dropdownColor: Colors.white,
      value: selectedOption,
      icon: const Icon(Icons.person_sharp),
      iconSize: 28,
      style: titleLarge(context),
      onChanged: (value) {
        setState(() {
          selectedOption = value ?? walletOptions.first;
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

  OptionCard({required this.optionText});

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

// FutureBuilder<dynamic>(
//               future: getKeplrAddress(),
//               builder: ((context, snapshot) {
//                 if (snapshot.hasData) {
//                   print("Wallet Address: ${snapshot.data}");
//                   return IconButton(onPressed: () {}, icon: Icon(Icons.wallet));
//                 } else {
//                   return IconButton(
//                       onPressed: () {}, icon: Icon(Icons.construction));
//                 }
//               }))