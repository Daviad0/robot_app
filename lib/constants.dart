import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sparkclub/popupwidgets/myaccount.dart';
import 'package:sparkclub/popupwidgets/settings.dart';
import 'package:sparkclub/signin.dart';

abstract class Constants {
  static const String appTitle = 'SparkClub';
  static const Color seedColor = Color(0xFF0056d2);
  static const Color darkSeedColor = Color(0xFFb2c5ff);

  static List<PopupMenuEntry<int>> popupMenuItems = [
    PopupMenuItem(
      value: 0,
      child: Row(
        children: const <Widget>[
          Icon(Icons.account_circle, color: Colors.black),
          SizedBox(width: 8),
          Text('My Account'),
        ],
      ),
    ),
    PopupMenuItem<int>(
      value: 1,
      child: Row(
        children: const <Widget>[
          Icon(Icons.settings, color: Colors.black),
          SizedBox(width: 8),
          Text('Settings'),
        ],
      ),
    ),
    PopupMenuItem<int>(
      value: 2,
      child: Row(
        children: const <Widget>[
          Icon(Icons.exit_to_app, color: Colors.black),
          SizedBox(width: 8),
          Text('Sign Out'),
        ],
      ),
    ),
  ];

  static const List<BottomNavigationBarItem> bottomNavItems = [
    BottomNavigationBarItem(
      icon: Icon(Icons.home),
      label: 'Home',
    ),
    BottomNavigationBarItem(
      icon: Icon(Icons.check_circle_outline_outlined),
      label: 'Meetings',
    ),
  ];
}

abstract class FunctionConstants {
  static List<Function> popupMenuFunctions = [
    (context) => Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => const MyAccount(),
      ),
    ),
    (context) => Navigator.of(context).push(
      MaterialPageRoute(
        builder: (context) => const Settings(),
      ),
    ),
    (context) async {
      SharedPreferences prefs = await SharedPreferences.getInstance();
      prefs.remove(StorageConstants.usernameKey);
      Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (BuildContext ctx) => const SignIn())
      );
    },
  ];
}

abstract class StorageConstants {
  static const String usernameKey = 'username';
}