import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sparkclub/dropdown/myaccount.dart';
import 'package:sparkclub/dropdown/settings.dart';
import 'package:sparkclub/signin.dart';

abstract class Constants {
  static const String appTitle = 'SparkClub';
  static const Color seedColor = Color(0xFF323996);
  static const Color darkSeedColor = Color(0xFFb2c5ff);
  static final Color textColor = Colors.indigo.shade900;

  static final List<PopupMenuEntry<int>> popupMenuItems = [
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
    const PopupMenuDivider(),
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
  static final List<Function> popupMenuFunctions = [
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
      // TODO: fix this, it looks ugly
      showDialog(
        context: context,
        builder: (ctx) => AlertDialog(
          title: const Text('Are you sure you want to sign out?'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: const <Widget>[
              Text('You will have to re-enter your information!'),
            ],
          ),
          actions: <Widget>[
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                primary: Theme.of(context).colorScheme.error,
                onPrimary: Theme.of(context).colorScheme.onError,
              ),
              onPressed: () {
                () async {
                  SharedPreferences prefs = await SharedPreferences.getInstance();
                  prefs.remove(StorageConstants.usernameKey);
                }();
                Navigator.of(context).pushReplacement(
                  MaterialPageRoute(builder: (BuildContext ctx) => const SignIn())
                );
              },
              child: const Text('Sign Out'),
            ),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                primary: Theme.of(context).colorScheme.secondary,
                onPrimary: Theme.of(context).colorScheme.onSecondary,
              ),
              onPressed: () => Navigator.of(context).pop(),
              child: const Text('Cancel'),
            ),
          ],
        ),
      );
    },
  ];
  static void showUnfinishedSnackbar(BuildContext context) {
    ScaffoldMessenger.of(context).clearSnackBars();
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('This feature has not been implemented!'),
        backgroundColor: Theme.of(context).colorScheme.error,
      ),
    );
  }
}

abstract class StorageConstants {
  static const String usernameKey = 'username';
}