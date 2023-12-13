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

Future<String> getKeplrAddress() async {
  const String chainId = "injective-888";
  if (js.context.hasProperty('getOfflineSigner') &&
      js.context.hasProperty('keplr')) {
    try {
      final account = js.context.callMethod('getKeplrAccount', [chainId]);
      return await promiseToFuture<String>(account);
    } catch (error) {
      // Handle any errors that occur during the connection
      if (kDebugMode) {
        print('Error getting Keplr account: $error');
      }
      return Future.error(error.toString());
    }
  } else {
    // Keplr extension is not installed
    return Future.error('Keplr is not available');
  }
}
