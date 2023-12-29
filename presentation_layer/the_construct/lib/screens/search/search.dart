import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:nil/nil.dart';
import 'package:the_construct/models/robot_catalog/robot_catalog_model.dart';
import 'package:the_construct/services/navigation/navigation.dart';
import 'package:the_construct/size_config/size_config.dart';

import '../../bloc/generics/generic_bloc.dart';
import '../../bloc/generics/generic_state.dart';
import '../../bloc/generics/generics_event.dart';
import '../../repositories/robot_repository.dart';

class CustomSearchBar extends StatefulWidget {
  const CustomSearchBar({super.key, this.recentResults});
  final List<RobotDetails>? recentResults;

  @override
  CustomSearchBarState createState() => CustomSearchBarState();
}

class CustomSearchBarState extends State<CustomSearchBar> {
  TextEditingController _controller = TextEditingController();
  List<RobotDetails> _results = <RobotDetails>[];
  bool _isSearching = false;
  late GenericBloc<RobotDetails, RobotDetailsRepository> bloc;

  @override
  void initState() {
    bloc = BlocProvider.of<GenericBloc<RobotDetails, RobotDetailsRepository>>(
        context);
    bloc.add(LoadingGenericData());
    _controller = TextEditingController();
    super.initState();
  }

  @override
  void dispose() {
    bloc.close();
    _controller.dispose();

    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
        child: Padding(
            padding: const EdgeInsets.only(top:8.0),
            child: BlocBuilder<
                GenericBloc<RobotDetails, RobotDetailsRepository>,
                GenericState>(
              builder: (BuildContext context, GenericState state) {
                if (state is LoadingState) {
                  return Column(
                    children: <Widget>[
                      Padding(
                        padding: const EdgeInsets.all(8.0),
                        child: AnimatedContainer(
                          duration: const Duration(milliseconds: 300),
                          curve: Curves.easeInOut,
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.circular(30.0),
                            color: Colors.grey[300],
                          ),
                          child: Row(
                            children: <Widget>[
                              const Padding(
                                padding: EdgeInsets.only(left: 8.0),
                                child: Icon(Icons.search),
                              ),
                              Expanded(
                                child: TextField(
                                  controller: _controller,
                                  decoration: const InputDecoration(
                                    hintText:
                                        'Searching database...',
                                    border: InputBorder.none,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  );
                } else if (state is HasDataState) {
                  final List<RobotDetails> data =
                      state.data as List<RobotDetails>;
                  return SizedBox(
                    height: SizeConfig.screenHeight * .2,
                    child: Column(
                      children: <Widget>[
                        Padding(
                          padding: const EdgeInsets.all(8.0),
                          child: AnimatedContainer(
                            duration: const Duration(milliseconds: 300),
                            curve: Curves.easeInOut,
                            decoration: BoxDecoration(
                              borderRadius: BorderRadius.circular(30.0),
                              color: Colors.grey[300],
                            ),
                            child: Row(
                              children: <Widget>[
                                const Padding(
                                  padding: EdgeInsets.only(left: 8.0),
                                  child: Icon(Icons.search),
                                ),
                                Expanded(
                                  child: TextField(
                                    controller: _controller,
                                    onChanged: (String value) async {
                                      if (value.length >= 2) {
                                        setState(() {
                                          _isSearching = true;
                                        });
                                        final List<RobotDetails> results = data;
                                        setState(() {
                                          try {
                                            _results = results
                                                .where((RobotDetails result) =>
                                                    result.model
                                                        .toLowerCase()
                                                        .contains(_controller
                                                            .text
                                                            .toLowerCase()) ||
                                                    result.manufacturer
                                                        .toLowerCase()
                                                        .contains(_controller
                                                            .text
                                                            .toLowerCase()))
                                                .toList();
                                          } catch (e) {
                                            if (kDebugMode) {
                                              print(e);
                                            }
                                          }
                                        });
                                      } else {
                                        setState(() {
                                          _isSearching = false;
                                        });
                                      }
                                    },
                                    onSubmitted: (String value) async {
                                      final List<RobotDetails> results = data;
                                      try {
                                        // ignore: no_leading_underscores_for_local_identifiers
                                        final RobotDetails _result = results
                                            .where((RobotDetails result) =>
                                                result.model
                                                    .toLowerCase()
                                                    .contains(
                                                        value.toLowerCase()))
                                            .first;
                                        router.goNamed('modelDetails',
                                            extra: _result);
                                      } catch (e) {
                                        if (kDebugMode) {
                                          print(e);
                                        }
                                      }
                                    },
                                    decoration: const InputDecoration(
                                      hintText: 'Search',
                                      border: InputBorder.none,
                                    ),
                                  ),
                                ),
                                if (_isSearching)
                                  IconButton(
                                    icon: const Icon(Icons.cancel),
                                    onPressed: () {
                                      setState(() {
                                        _controller.clear();
                                        _results.clear();
                                        _isSearching = false;
                                        // Remove focus from TextField
                                        FocusScope.of(context).unfocus();
                                      });
                                    },
                                  )
                                else
                                  const SizedBox.shrink(),
                              ],
                            ),
                          ),
                        ),
                        if (_results.isNotEmpty)
                          Expanded(
                            child: ListView.builder(
                              itemCount: _results.length,
                              itemBuilder: (BuildContext context, int index) {
                                final RobotDetails result = _results[index];
                                return ListTile(
                                  title: Text(result.model),
                                  subtitle: Text(result.manufacturer),
                                  onTap: () {
                                    setState(() {
                                      widget.recentResults?.insert(0, result);
                                      _controller.text = result.model;
                                      _results.clear();
                                      // _isSearching = false;
                                      // // Remove focus from TextField
                                      // FocusScope.of(context).unfocus();
                                    });
                                    router.goNamed('robotDetails',pathParameters: {"model_id":result.model_id},
                                        extra: result);
                                  },
                                );
                              },
                            ),
                          )
                        else
                          const SizedBox.shrink(),
                        if (widget.recentResults?.isNotEmpty ?? false)
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: <Widget>[
                              const Padding(
                                padding: EdgeInsets.only(left: 16.0),
                                child: Text('Recents'),
                              ),
                              ...widget.recentResults!
                                  .map((RobotDetails recent) => ListTile(
                                        title: Text(recent.model),
                                        onTap: () {
                                          setState(() {
                                            _controller.text = recent.model;
                                            _results.clear();
                                          });
                                        },
                                      )),
                            ],
                          )
                        else
                          const SizedBox.shrink(),
                      ],
                    ),
                  );
                } else {
                  return nil;
                }
              },
            )));
  }
}
