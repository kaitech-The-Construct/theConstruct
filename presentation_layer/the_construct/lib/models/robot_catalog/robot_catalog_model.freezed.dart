// coverage:ignore-file
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'robot_catalog_model.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

T _$identity<T>(T value) => value;

final _privateConstructorUsedError = UnsupportedError(
    'It seems like you constructed your class using `MyClass._()`. This constructor is only meant to be used by freezed and you are not supposed to need it nor use it.\nPlease check the documentation here for more information: https://github.com/rrousselGit/freezed#custom-getters-and-methods');

RobotDetails _$RobotDetailsFromJson(Map<String, dynamic> json) {
  return _RobotDetails.fromJson(json);
}

/// @nodoc
mixin _$RobotDetails {
  String get manufacturer => throw _privateConstructorUsedError;
  String get manufacturer_id => throw _privateConstructorUsedError;
  String get model => throw _privateConstructorUsedError;
  String get model_id => throw _privateConstructorUsedError;
  PriceDetails get price => throw _privateConstructorUsedError;
  String get description => throw _privateConstructorUsedError;
  String? get image_url => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $RobotDetailsCopyWith<RobotDetails> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $RobotDetailsCopyWith<$Res> {
  factory $RobotDetailsCopyWith(
          RobotDetails value, $Res Function(RobotDetails) then) =
      _$RobotDetailsCopyWithImpl<$Res, RobotDetails>;
  @useResult
  $Res call(
      {String manufacturer,
      String manufacturer_id,
      String model,
      String model_id,
      PriceDetails price,
      String description,
      String? image_url});

  $PriceDetailsCopyWith<$Res> get price;
}

/// @nodoc
class _$RobotDetailsCopyWithImpl<$Res, $Val extends RobotDetails>
    implements $RobotDetailsCopyWith<$Res> {
  _$RobotDetailsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? manufacturer = null,
    Object? manufacturer_id = null,
    Object? model = null,
    Object? model_id = null,
    Object? price = null,
    Object? description = null,
    Object? image_url = freezed,
  }) {
    return _then(_value.copyWith(
      manufacturer: null == manufacturer
          ? _value.manufacturer
          : manufacturer // ignore: cast_nullable_to_non_nullable
              as String,
      manufacturer_id: null == manufacturer_id
          ? _value.manufacturer_id
          : manufacturer_id // ignore: cast_nullable_to_non_nullable
              as String,
      model: null == model
          ? _value.model
          : model // ignore: cast_nullable_to_non_nullable
              as String,
      model_id: null == model_id
          ? _value.model_id
          : model_id // ignore: cast_nullable_to_non_nullable
              as String,
      price: null == price
          ? _value.price
          : price // ignore: cast_nullable_to_non_nullable
              as PriceDetails,
      description: null == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
              as String,
      image_url: freezed == image_url
          ? _value.image_url
          : image_url // ignore: cast_nullable_to_non_nullable
              as String?,
    ) as $Val);
  }

  @override
  @pragma('vm:prefer-inline')
  $PriceDetailsCopyWith<$Res> get price {
    return $PriceDetailsCopyWith<$Res>(_value.price, (value) {
      return _then(_value.copyWith(price: value) as $Val);
    });
  }
}

/// @nodoc
abstract class _$$RobotDetailsImplCopyWith<$Res>
    implements $RobotDetailsCopyWith<$Res> {
  factory _$$RobotDetailsImplCopyWith(
          _$RobotDetailsImpl value, $Res Function(_$RobotDetailsImpl) then) =
      __$$RobotDetailsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call(
      {String manufacturer,
      String manufacturer_id,
      String model,
      String model_id,
      PriceDetails price,
      String description,
      String? image_url});

  @override
  $PriceDetailsCopyWith<$Res> get price;
}

/// @nodoc
class __$$RobotDetailsImplCopyWithImpl<$Res>
    extends _$RobotDetailsCopyWithImpl<$Res, _$RobotDetailsImpl>
    implements _$$RobotDetailsImplCopyWith<$Res> {
  __$$RobotDetailsImplCopyWithImpl(
      _$RobotDetailsImpl _value, $Res Function(_$RobotDetailsImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? manufacturer = null,
    Object? manufacturer_id = null,
    Object? model = null,
    Object? model_id = null,
    Object? price = null,
    Object? description = null,
    Object? image_url = freezed,
  }) {
    return _then(_$RobotDetailsImpl(
      manufacturer: null == manufacturer
          ? _value.manufacturer
          : manufacturer // ignore: cast_nullable_to_non_nullable
              as String,
      manufacturer_id: null == manufacturer_id
          ? _value.manufacturer_id
          : manufacturer_id // ignore: cast_nullable_to_non_nullable
              as String,
      model: null == model
          ? _value.model
          : model // ignore: cast_nullable_to_non_nullable
              as String,
      model_id: null == model_id
          ? _value.model_id
          : model_id // ignore: cast_nullable_to_non_nullable
              as String,
      price: null == price
          ? _value.price
          : price // ignore: cast_nullable_to_non_nullable
              as PriceDetails,
      description: null == description
          ? _value.description
          : description // ignore: cast_nullable_to_non_nullable
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
class _$RobotDetailsImpl implements _RobotDetails {
  _$RobotDetailsImpl(
      {required this.manufacturer,
      required this.manufacturer_id,
      required this.model,
      required this.model_id,
      required this.price,
      required this.description,
      this.image_url});

  factory _$RobotDetailsImpl.fromJson(Map<String, dynamic> json) =>
      _$$RobotDetailsImplFromJson(json);

  @override
  final String manufacturer;
  @override
  final String manufacturer_id;
  @override
  final String model;
  @override
  final String model_id;
  @override
  final PriceDetails price;
  @override
  final String description;
  @override
  final String? image_url;

  @override
  String toString() {
    return 'RobotDetails(manufacturer: $manufacturer, manufacturer_id: $manufacturer_id, model: $model, model_id: $model_id, price: $price, description: $description, image_url: $image_url)';
  }

  @override
  bool operator ==(dynamic other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$RobotDetailsImpl &&
            (identical(other.manufacturer, manufacturer) ||
                other.manufacturer == manufacturer) &&
            (identical(other.manufacturer_id, manufacturer_id) ||
                other.manufacturer_id == manufacturer_id) &&
            (identical(other.model, model) || other.model == model) &&
            (identical(other.model_id, model_id) ||
                other.model_id == model_id) &&
            (identical(other.price, price) || other.price == price) &&
            (identical(other.description, description) ||
                other.description == description) &&
            (identical(other.image_url, image_url) ||
                other.image_url == image_url));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode => Object.hash(runtimeType, manufacturer, manufacturer_id,
      model, model_id, price, description, image_url);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$RobotDetailsImplCopyWith<_$RobotDetailsImpl> get copyWith =>
      __$$RobotDetailsImplCopyWithImpl<_$RobotDetailsImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$RobotDetailsImplToJson(
      this,
    );
  }
}

abstract class _RobotDetails implements RobotDetails {
  factory _RobotDetails(
      {required final String manufacturer,
      required final String manufacturer_id,
      required final String model,
      required final String model_id,
      required final PriceDetails price,
      required final String description,
      final String? image_url}) = _$RobotDetailsImpl;

  factory _RobotDetails.fromJson(Map<String, dynamic> json) =
      _$RobotDetailsImpl.fromJson;

  @override
  String get manufacturer;
  @override
  String get manufacturer_id;
  @override
  String get model;
  @override
  String get model_id;
  @override
  PriceDetails get price;
  @override
  String get description;
  @override
  String? get image_url;
  @override
  @JsonKey(ignore: true)
  _$$RobotDetailsImplCopyWith<_$RobotDetailsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}

PriceDetails _$PriceDetailsFromJson(Map<String, dynamic> json) {
  return _PriceDetails.fromJson(json);
}

/// @nodoc
mixin _$PriceDetails {
  String get model => throw _privateConstructorUsedError;
  double get subscription_price => throw _privateConstructorUsedError;
  double? get listing_price => throw _privateConstructorUsedError;

  Map<String, dynamic> toJson() => throw _privateConstructorUsedError;
  @JsonKey(ignore: true)
  $PriceDetailsCopyWith<PriceDetails> get copyWith =>
      throw _privateConstructorUsedError;
}

/// @nodoc
abstract class $PriceDetailsCopyWith<$Res> {
  factory $PriceDetailsCopyWith(
          PriceDetails value, $Res Function(PriceDetails) then) =
      _$PriceDetailsCopyWithImpl<$Res, PriceDetails>;
  @useResult
  $Res call({String model, double subscription_price, double? listing_price});
}

/// @nodoc
class _$PriceDetailsCopyWithImpl<$Res, $Val extends PriceDetails>
    implements $PriceDetailsCopyWith<$Res> {
  _$PriceDetailsCopyWithImpl(this._value, this._then);

  // ignore: unused_field
  final $Val _value;
  // ignore: unused_field
  final $Res Function($Val) _then;

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? model = null,
    Object? subscription_price = null,
    Object? listing_price = freezed,
  }) {
    return _then(_value.copyWith(
      model: null == model
          ? _value.model
          : model // ignore: cast_nullable_to_non_nullable
              as String,
      subscription_price: null == subscription_price
          ? _value.subscription_price
          : subscription_price // ignore: cast_nullable_to_non_nullable
              as double,
      listing_price: freezed == listing_price
          ? _value.listing_price
          : listing_price // ignore: cast_nullable_to_non_nullable
              as double?,
    ) as $Val);
  }
}

/// @nodoc
abstract class _$$PriceDetailsImplCopyWith<$Res>
    implements $PriceDetailsCopyWith<$Res> {
  factory _$$PriceDetailsImplCopyWith(
          _$PriceDetailsImpl value, $Res Function(_$PriceDetailsImpl) then) =
      __$$PriceDetailsImplCopyWithImpl<$Res>;
  @override
  @useResult
  $Res call({String model, double subscription_price, double? listing_price});
}

/// @nodoc
class __$$PriceDetailsImplCopyWithImpl<$Res>
    extends _$PriceDetailsCopyWithImpl<$Res, _$PriceDetailsImpl>
    implements _$$PriceDetailsImplCopyWith<$Res> {
  __$$PriceDetailsImplCopyWithImpl(
      _$PriceDetailsImpl _value, $Res Function(_$PriceDetailsImpl) _then)
      : super(_value, _then);

  @pragma('vm:prefer-inline')
  @override
  $Res call({
    Object? model = null,
    Object? subscription_price = null,
    Object? listing_price = freezed,
  }) {
    return _then(_$PriceDetailsImpl(
      model: null == model
          ? _value.model
          : model // ignore: cast_nullable_to_non_nullable
              as String,
      subscription_price: null == subscription_price
          ? _value.subscription_price
          : subscription_price // ignore: cast_nullable_to_non_nullable
              as double,
      listing_price: freezed == listing_price
          ? _value.listing_price
          : listing_price // ignore: cast_nullable_to_non_nullable
              as double?,
    ));
  }
}

/// @nodoc
@JsonSerializable()
class _$PriceDetailsImpl implements _PriceDetails {
  _$PriceDetailsImpl(
      {required this.model,
      required this.subscription_price,
      this.listing_price});

  factory _$PriceDetailsImpl.fromJson(Map<String, dynamic> json) =>
      _$$PriceDetailsImplFromJson(json);

  @override
  final String model;
  @override
  final double subscription_price;
  @override
  final double? listing_price;

  @override
  String toString() {
    return 'PriceDetails(model: $model, subscription_price: $subscription_price, listing_price: $listing_price)';
  }

  @override
  bool operator ==(dynamic other) {
    return identical(this, other) ||
        (other.runtimeType == runtimeType &&
            other is _$PriceDetailsImpl &&
            (identical(other.model, model) || other.model == model) &&
            (identical(other.subscription_price, subscription_price) ||
                other.subscription_price == subscription_price) &&
            (identical(other.listing_price, listing_price) ||
                other.listing_price == listing_price));
  }

  @JsonKey(ignore: true)
  @override
  int get hashCode =>
      Object.hash(runtimeType, model, subscription_price, listing_price);

  @JsonKey(ignore: true)
  @override
  @pragma('vm:prefer-inline')
  _$$PriceDetailsImplCopyWith<_$PriceDetailsImpl> get copyWith =>
      __$$PriceDetailsImplCopyWithImpl<_$PriceDetailsImpl>(this, _$identity);

  @override
  Map<String, dynamic> toJson() {
    return _$$PriceDetailsImplToJson(
      this,
    );
  }
}

abstract class _PriceDetails implements PriceDetails {
  factory _PriceDetails(
      {required final String model,
      required final double subscription_price,
      final double? listing_price}) = _$PriceDetailsImpl;

  factory _PriceDetails.fromJson(Map<String, dynamic> json) =
      _$PriceDetailsImpl.fromJson;

  @override
  String get model;
  @override
  double get subscription_price;
  @override
  double? get listing_price;
  @override
  @JsonKey(ignore: true)
  _$$PriceDetailsImplCopyWith<_$PriceDetailsImpl> get copyWith =>
      throw _privateConstructorUsedError;
}
