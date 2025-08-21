
import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

ThemeData appThemeData = ThemeData(
  // Define the default brightness and colors.
  primaryColor: const Color(0xFF115511), // Replace with your primary color hex code
  // accentColor: Color(0xFF654321), // Replace with your accent color hex code
  // backgroundColor: Color(0xFFF3F3F3), // Replace with your background color hex code
  scaffoldBackgroundColor: const Color(0xFFFFFFFF), // Replace with your scaffold background color hex code

  // Define the default TextTheme. Use this to specify the default
  // text styling for headlines, titles, bodies of text, and more.
  textTheme: GoogleFonts.robotoTextTheme(const TextTheme(
    displayLarge: TextStyle(fontSize: 72.0, fontWeight: FontWeight.bold),
    titleLarge: TextStyle(fontSize: 36.0, fontStyle: FontStyle.italic),
    bodyLarge: TextStyle(fontSize: 16.0, fontFamily: 'Hind', color: Color(0xFF333333)),
    bodyMedium: TextStyle(fontSize: 14.0, fontFamily: 'Hind', color: Color(0xFF666666)),
  ),),

  // Define the default ButtonThemeData. Use this to specify default
  // button themes.
  buttonTheme: ButtonThemeData(
    buttonColor: const Color(0xFF007BFF),     // Default color for primary buttons
    shape: RoundedRectangleBorder(
      borderRadius: BorderRadius.circular(8.0),
    ),
  ),

  // Define static colors you might use in other areas of the app
  colorScheme: const ColorScheme(
    primary: Color(0xFF007BFF),
    primaryContainer: Color(0xFF0056b3),
    secondary: Color(0xFF00D2C2),
    secondaryContainer: Color(0xFF00a192),
    surface: Color(0xFFE9EEF3),
    error: Color(0xFFDC3545),
    onPrimary: Colors.white,
    onSecondary: Colors.white,
    onSurface: Color(0xFF333333),
    onError: Colors.white,
    brightness: Brightness.light,
  ),

  // Include any additional theming, such as the color of the AppBar
  appBarTheme: const AppBarTheme(
   backgroundColor: Colors.white, // Replace with your app bar color hex code
   iconTheme: IconThemeData(color: Color(0xFF123456)),
   elevation: 0,
    titleTextStyle: 
     TextStyle(color: Color(0xFFFFFFFF), fontSize: 20), // App Bar title style
     actionsIconTheme: IconThemeData(color: Color(0xFF123456),
     
     )
    
  ),

  // Use this to style the FloatingActionButton
  floatingActionButtonTheme: const FloatingActionButtonThemeData(
  ),

  // You can add slider themes, icon themes, etc. here as well.
);