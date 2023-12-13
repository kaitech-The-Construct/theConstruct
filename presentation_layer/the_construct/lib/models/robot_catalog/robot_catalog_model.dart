// ignore_for_file: non_constant_identifier_names

import 'package:freezed_annotation/freezed_annotation.dart';

part 'robot_catalog_model.freezed.dart';
part 'robot_catalog_model.g.dart';

@freezed
class RobotDetails with _$RobotDetails {
  factory RobotDetails({
    required String manufacturer,
    required String manufacturer_id,
    required String model,
    required String model_id,
    required PriceDetails price,
    required String description,
    String? image_url,
  }) = _RobotDetails;
  factory RobotDetails.fromJson(Map<String, Object?> json) =>
      _$RobotDetailsFromJson(json);
}

@freezed
class PriceDetails with _$PriceDetails {
  factory PriceDetails({
    required String model,
    required double subscription_price,
    double? listing_price,
  }) = _PriceDetails;
  factory PriceDetails.fromJson(Map<String, Object?> json) =>
      _$PriceDetailsFromJson(json);
}


// dart run build_runner build