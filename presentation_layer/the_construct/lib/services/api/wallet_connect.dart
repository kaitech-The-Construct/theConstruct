// ignore_for_file: avoid_web_libraries_in_flutter

import 'dart:async';
import 'dart:js' as js;
import 'dart:js_util';
import 'package:flutter/foundation.dart';
import 'package:js/js.dart';

@JS()
external dynamic getAccount();

Future<String?> getEthAddressFromMetaMask() async {
  // Ensure MetaMask is available
  if (js.context.hasProperty('ethereum')) {
    try {
      final response = getAccount();
      final account = await promiseToFuture<String?>(response);
      return account;
    } catch (error) {
      // Handle errors, such as the user refusing the connection
      if (kDebugMode) {
        print('Error getting Ethereum account: $error');
      }
      return null; // Return null or handle the error as needed
    }
  } else {
    return null; // Return null or handle the case where MetaMask is not available
  }
}

Future<String?> getKeplrAddress() async {
  // Ensure Keplr is available
  if (js.context.hasProperty('getOfflineSigner') &&
      js.context.hasProperty('keplr')) {
    try {
      final account = await js.context.callMethod('getKeplrAccount');
      return account.toString();
    } catch (error) {
      // Handle any errors that occur during the connection
      if (kDebugMode) {
        print('Error getting Keplr account: $error');
      }
      return null;
    }
  } else {
    // Keplr extension is not installed
    return null;
  }
}
