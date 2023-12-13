import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/foundation.dart';

import '../bloc/generics/generic_bloc.dart';
import '../models/robot_catalog/robot_catalog_model.dart';

class RobotDetailsRepository extends GenericBlocRepository<RobotDetails> {
  @override
  Stream<List<RobotDetails>> data() {
    final Query<Object> robotDetailsCollection =
        FirebaseFirestore.instance.collection('test_robots');

    // Get all Quick Facts
    List<RobotDetails> robotListFromSnapshot(QuerySnapshot<Object> snapshot) {
      try {
        final List<RobotDetails> robotList =
            snapshot.docs.map((QueryDocumentSnapshot<Object> doc) {
          return RobotDetails.fromJson(doc.data() as Map<String, dynamic>);
        }).toList();
        
        return robotList;
      } catch (e) {
        if (kDebugMode) {
          print('Error in Robot Data Repository: $e');
        }
        return <RobotDetails>[];
      }
    }

    return robotDetailsCollection.snapshots().map(robotListFromSnapshot);
  }
}
