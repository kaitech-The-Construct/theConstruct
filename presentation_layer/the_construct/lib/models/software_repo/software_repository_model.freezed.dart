// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'software_repository_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#custom-getters-and-methods');

SoftwareDetails _$SoftwareDetailsFromJson(Map<String, dynamic> json) {
  return _SoftwareDetails.fromJson(json);
}

/// @nodoc
mixin _$SoftwareDetails {
  String get name => throw _privateConstructorUsedError;
  String get version => throw _privateConstructorUsedError;
  String get author => throw _privateConstructorUsedError;
  String get description => throw _privateConstructorUsedError;
  List<String> get compatibility => throw _privateConstructorUsedError;
  String get license => throw _privateConstructorUsedError;
  String? get image_url => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $SoftwareDetailsCopyWith<SoftwareDetails> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $SoftwareDetailsCopyWith<$Res> {
  factory $SoftwareDetailsCopyWith(
          SoftwareDetails value, $Res Function(SoftwareDetails) then) =
      _$SoftwareDetailsCopyWithImpl<$Res, SoftwareDetails>;
  @useResult
  $Res call(
      {String name,
      String version,
      String author,
      String description,
      List<String> compatibility,
      String license,
      String? image_url});
}

/// @nodoc
class _$SoftwareDetailsCopyWithImpl<$Res, $Val extends SoftwareDetails>
    implements $SoftwareDetailsCopyWith<$Res> {
  _$SoftwareDetailsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = null,
    Object? version = null,
    Object? author = null,
    Object? description = null,
    Object? compatibility = null,
    Object? license = null,
    Object? image_url = freezed,
  }) {
    return _then(_value.copyWith(
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      version: null == version
          ? _value.version
          : version // ignore: cast_nullable_to_non_nullable
              as String,
      author: null == author
          ? _value.author
          : author // ignore: cast_nullable_to_non_nullable
              as String,
      description: null == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String,
      compatibility: null == compatibility
          ? _value.compatibility
          : compatibility // ignore: cast_nullable_to_non_nullable
              as List<String>,
      license: null == license
          ? _value.license
          : license // ignore: cast_nullable_to_non_nullable
              as String,
      image_url: freezed == image_url
          ? _value.image_url
          : image_url // ignore: cast_nullable_to_non_nullable
              as String?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$SoftwareDetailsImplCopyWith<$Res>
    implements $SoftwareDetailsCopyWith<$Res> {
  factory _$$SoftwareDetailsImplCopyWith(_$SoftwareDetailsImpl value,
          $Res Function(_$SoftwareDetailsImpl) then) =
      __$$SoftwareDetailsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {String name,
      String version,
      String author,
      String description,
      List<String> compatibility,
      String license,
      String? image_url});
}

/// @nodoc
class __$$SoftwareDetailsImplCopyWithImpl<$Res>
    extends _$SoftwareDetailsCopyWithImpl<$Res, _$SoftwareDetailsImpl>
    implements _$$SoftwareDetailsImplCopyWith<$Res> {
  __$$SoftwareDetailsImplCopyWithImpl(
      _$SoftwareDetailsImpl _value, $Res Function(_$SoftwareDetailsImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? name = null,
    Object? version = null,
    Object? author = null,
    Object? description = null,
    Object? compatibility = null,
    Object? license = null,
    Object? image_url = freezed,
  }) {
    return _then(_$SoftwareDetailsImpl(
      name: null == name
          ? _value.name
          : name // ignore: cast_nullable_to_non_nullable
              as String,
      version: null == version
          ? _value.version
          : version // ignore: cast_nullable_to_non_nullable
              as String,
      author: null == author
          ? _value.author
          : author // ignore: cast_nullable_to_non_nullable
              as String,
      description: null == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String,
      compatibility: null == compatibility
          ? _value._compatibility
          : compatibility // ignore: cast_nullable_to_non_nullable
              as List<String>,
      license: null == license
          ? _value.license
          : license // ignore: cast_nullable_to_non_nullable
              as String,
      image_url: freezed == image_url
          ? _value.image_url
          : image_url // ignore: cast_nullable_to_non_nullable
              as String?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$SoftwareDetailsImpl implements _SoftwareDetails {
  _$SoftwareDetailsImpl(
      {required this.name,
      required this.version,
      required this.author,
      required this.description,
      required final List<String> compatibility,
      required this.license,
      this.image_url})
      : _compatibility = compatibility;

  factory _$SoftwareDetailsImpl.fromJson(Map<String, dynamic> json) =>
      _$$SoftwareDetailsImplFromJson(json);

  @override
  final String name;
  @override
  final String version;
  @override
  final String author;
  @override
  final String description;
  final List<String> _compatibility;
  @override
  List<String> get compatibility {
    if (_compatibility is EqualUnmodifiableListView) return _compatibility;
    // ignore: implicit_dynamic_type
    return EqualUnmodifiableListView(_compatibility);
  }

  @override
  final String license;
  @override
  final String? image_url;

  @override
  String toString() {
    return 'SoftwareDetails(name: $name, version: $version, author: $author, description: $description, compatibility: $compatibility, license: $license, image_url: $image_url)';
  }

  @override
  bool operator ==(dynamic other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$SoftwareDetailsImpl &&
            (identical(other.name, name) || other.name == name) &&
            (identical(other.version, version) || other.version == version) &&
            (identical(other.author, author) || other.author == author) &&
            (identical(other.description, description) ||
                other.description == description) &&
            const DeepCollectionEquality()
                .equals(other._compatibility, _compatibility) &&
            (identical(other.license, license) || other.license == license) &&
            (identical(other.image_url, image_url) ||
                other.image_url == image_url));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(
      runtimeType,
      name,
      version,
      author,
      description,
      const DeepCollectionEquality().hash(_compatibility),
      license,
      image_url);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$SoftwareDetailsImplCopyWith<_$SoftwareDetailsImpl> get copyWith =>
      __$$SoftwareDetailsImplCopyWithImpl<_$SoftwareDetailsImpl>(
          this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$SoftwareDetailsImplToJson(
      this,
    );
  }
}

abstract class _SoftwareDetails implements SoftwareDetails {
  factory _SoftwareDetails(
      {required final String name,
      required final String version,
      required final String author,
      required final String description,
      required final List<String> compatibility,
      required final String license,
      final String? image_url}) = _$SoftwareDetailsImpl;

  factory _SoftwareDetails.fromJson(Map<String, dynamic> json) =
      _$SoftwareDetailsImpl.fromJson;

  @override
  String get name;
  @override
  String get version;
  @override
  String get author;
  @override
  String get description;
  @override
  List<String> get compatibility;
  @override
  String get license;
  @override
  String? get image_url;
  @override
  @JsonKey(ignore: true)
  _$$SoftwareDetailsImplCopyWith<_$SoftwareDetailsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
