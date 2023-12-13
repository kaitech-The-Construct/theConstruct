import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter_web3/flutter_web3.dart';
import 'package:http/http.dart' as http;
import 'package:the_construct/models/robot_catalog/robot_catalog_model.dart';
import 'package:the_construct/models/software_repo/software_repository_model.dart';
// import 'package:web3dart/browser.dart'; // Use this import for web-based applications

class APIFunctions {
  Future<List<RobotDetails>> getRobotList() async {
    try {
      // Call the Firebase Functions HTTP endpoint 'getRobotList'
      final http.Response callable = await http.get(
          Uri.parse('https://application-layer-bu6vz2kbtq-uc.a.run.app/robots/list'));

      // Parse the JSON response from the callable as a List of Maps
      final List<dynamic> response =
          json.decode(callable.body) as List<dynamic>;
      if (kDebugMode) {
        print(response);
      }
      // Convert the List of Maps to a List of RobotDetails objects using RobotDetails.fromJson()
      final List<RobotDetails> robotDetailsList = response
          .map((item) => RobotDetails.fromJson(item as Map<String, dynamic>))
          .toList();

      // Return the List of RobotDetails objects
      return robotDetailsList;
    } catch (e, stackTrace) {
      // Print an error message and return an empty List if an error occurs
      if (kDebugMode) {
        print('Error in getRobotList: $e, $stackTrace');
      }
      return <RobotDetails>[];
    }
  }

  Future<List<SoftwareDetails>> getSoftwareList() async {
    try {
      // Call the Firebase Functions HTTP endpoint 'getSoftwareList'
      final http.Response callable = await http.get(Uri.parse(
          'https://application-layer-bu6vz2kbtq-uc.a.run.app/software/list'));

      // Parse the JSON response from the callable as a List of Maps
      final List<dynamic> response =
          json.decode(callable.body) as List<dynamic>;
      // Convert the List of Maps to a List of SoftwareDetails objects using SoftwareDetails.fromJson()
      final List<SoftwareDetails> softwareDetailsList = response
          .map((item) => SoftwareDetails.fromJson(item as Map<String, dynamic>))
          .toList();

      // Return the List of SoftwareDetails objects
      return softwareDetailsList;
    } catch (e, stackTrace) {
      // Print an error message and return an empty List if an error occurs
      if (kDebugMode) {
        print('Error in getSoftwareList: $e, $stackTrace');
      }
      return <SoftwareDetails>[];
    }
  }

  final infuraUrl =
      'https://mainnet.infura.io/v3/7d2a5c43cf7949b08ae153fb15d32b07';
  final httpClient = http.Client();

  Future<void> connectWallet() async {
    try {
      final wc = WalletConnectProvider.fromInfura(infuraUrl);
      await wc.connect();

      if (wc.connected) {
        final web3provider = Web3Provider.fromWalletConnect(wc);
        print(web3provider); // Web3Provider:
      }
    } on Exception catch (e) {
      if (kDebugMode) {
        print(e);
      }
    }
  }
}
