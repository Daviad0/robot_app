import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sparkclub/constants.dart';
import 'package:sparkclub/homescreen.dart';
import 'package:sparkclub/signin.dart';

Future<void> main() async {
  // SharedPreferences.setMockInitialValues(<String, Object>{StorageConstants.usernameKey: 'quackings'});

  WidgetsFlutterBinding.ensureInitialized();
  SharedPreferences prefs = await SharedPreferences.getInstance();
  final username = prefs.getString(StorageConstants.usernameKey);
  runApp(MyApp(isLoggedIn: username != null));
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key, required this.isLoggedIn}) : super(key: key);
  final bool isLoggedIn;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: Constants.appTitle,
      theme: ThemeData.light().copyWith(
        colorScheme: ColorScheme.fromSeed(seedColor: Constants.seedColor),
      ),
      darkTheme: ThemeData.dark().copyWith(
        colorScheme: ColorScheme.fromSeed(seedColor: Constants.darkSeedColor),
      ),
      themeMode: ThemeMode.light,
      home: isLoggedIn ? const MainWidget() : const SignIn(),
    );
  }
}