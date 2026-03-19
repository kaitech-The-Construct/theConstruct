import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../bloc/product_bloc/product_bloc.dart';
import '../../bloc/cart_bloc/cart_bloc.dart';
import '../../models/product_model.dart';
import '../../services/api/api_client.dart';
import 'components/product_grid.dart';
import 'components/product_filters.dart';
import 'components/search_bar.dart';
import 'components/sort_options.dart';

class EnhancedMarketplace extends StatefulWidget {
  const EnhancedMarketplace({super.key});

  @override
  State<EnhancedMarketplace> createState() => _EnhancedMarketplaceState();
}

class _EnhancedMarketplaceState extends State<EnhancedMarketplace>
    with TickerProviderStateMixin {
  late TabController _tabController;
  late ScrollController _scrollController;
  
  String _searchQuery = '';
  Map<String, dynamic> _filters = {};
  String _sortBy = 'name';
  String _sortOrder = 'asc';
  bool _showFilters = false;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 6, vsync: this);
    _scrollController = ScrollController();
    
    // Load initial products
    context.read<ProductBloc>().add(LoadProducts());
  }

  @override
  void dispose() {
    _tabController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _onSearchChanged(String query) {
    setState(() {
      _searchQuery = query;
    });
    _performSearch();
  }

  void _onFiltersChanged(Map<String, dynamic> filters) {
    setState(() {
      _filters = filters;
    });
    _performSearch();
  }

  void _onSortChanged(String sortBy, String sortOrder) {
    setState(() {
      _sortBy = sortBy;
      _sortOrder = sortOrder;
    });
    _performSearch();
  }

  void _performSearch() {
    final searchFilters = {
      'query': _searchQuery,
      'sort_by': _sortBy,
      'sort_order': _sortOrder,
      ..._filters,
    };
    
    context.read<ProductBloc>().add(SearchProducts(searchFilters));
  }

  void _toggleFilters() {
    setState(() {
      _showFilters = !_showFilters;
    });
  }

  void _clearFilters() {
    setState(() {
      _searchQuery = '';
      _filters = {};
      _sortBy = 'name';
      _sortOrder = 'asc';
      _showFilters = false;
    });
    context.read<ProductBloc>().add(LoadProducts());
  }

  void _onProductTap(Product product) {
    Navigator.pushNamed(
      context,
      '/product-detail',
      arguments: product,
    );
  }

  void _onAddToCart(Product product) {
    context.read<CartBloc>().add(AddToCart(product, 1));
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
