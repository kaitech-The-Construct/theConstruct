import 'package:freezed_annotation/freezed_annotation.dart';

part 'software_repository_model.freezed.dart';
part 'software_repository_model.g.dart';

@freezed
class SoftwareDetails with _$SoftwareDetails {
  factory SoftwareDetails({
    required String name,
    required String version,
    required String author,
    required String description,
    required List<String> compatibility,
    required String license,
    String? image_url,
  }) = _SoftwareDetails;
  factory SoftwareDetails.fromJson(Map<String, Object?> json) =>
      _$SoftwareDetailsFromJson(json);
}
