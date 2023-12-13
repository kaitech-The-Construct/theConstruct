// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'robot_catalog_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$RobotDetailsImpl _$$RobotDetailsImplFromJson(Map<String, dynamic> json) =>
    _$RobotDetailsImpl(
      manufacturer: json['manufacturer'] as String,
      manufacturer_id: json['manufacturer_id'] as String,
      model: json['model'] as String,
      model_id: json['model_id'] as String,
      price: PriceDetails.fromJson(json['price'] as Map<String, dynamic>),
      description: json['description'] as String,
      image_url: json['image_url'] as String?,
    );

Map<String, dynamic> _$$RobotDetailsImplToJson(_$RobotDetailsImpl instance) =>
    <String, dynamic>{
      'manufacturer': instance.manufacturer,
      'manufacturer_id': instance.manufacturer_id,
      'model': instance.model,
      'model_id': instance.model_id,
      'price': instance.price,
      'description': instance.description,
      'image_url': instance.image_url,
    };

_$PriceDetailsImpl _$$PriceDetailsImplFromJson(Map<String, dynamic> json) =>
    _$PriceDetailsImpl(
      model: json['model'] as String,
      subscription_price: (json['subscription_price'] as num).toDouble(),
      listing_price: (json['listing_price'] as num?)?.toDouble(),
    );

Map<String, dynamic> _$$PriceDetailsImplToJson(_$PriceDetailsImpl instance) =>
    <String, dynamic>{
      'model': instance.model,
      'subscription_price': instance.subscription_price,
      'listing_price': instance.listing_price,
    };
