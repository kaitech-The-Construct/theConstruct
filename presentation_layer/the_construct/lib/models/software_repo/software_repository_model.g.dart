// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'software_repository_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_$SoftwareDetailsImpl _$$SoftwareDetailsImplFromJson(
        Map<String, dynamic> json) =>
    _$SoftwareDetailsImpl(
      name: json['name'] as String,
      version: json['version'] as String,
      author: json['author'] as String,
      description: json['description'] as String,
      compatibility: (json['compatibility'] as List<dynamic>)
          .map((e) => e as String)
          .toList(),
      license: json['license'] as String,
      image_url: json['image_url'] as String?,
    );

Map<String, dynamic> _$$SoftwareDetailsImplToJson(
        _$SoftwareDetailsImpl instance) =>
    <String, dynamic>{
      'name': instance.name,
      'version': instance.version,
      'author': instance.author,
      'description': instance.description,
      'compatibility': instance.compatibility,
      'license': instance.license,
      'image_url': instance.image_url,
    };
