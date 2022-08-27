import 'package:flutter/material.dart';

class Home extends StatelessWidget {
  const Home({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: const <Widget>[
          Text('Welcome to SparkClub!\nCurrently, nothing has been implemented, and you will also see this same screen across all tabs.', textAlign: TextAlign.center),
        ],
      ),
    );
  }
}