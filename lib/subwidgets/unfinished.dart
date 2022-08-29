import 'package:flutter/material.dart';

class Unfinished extends StatelessWidget {
  const Unfinished({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: const <Widget>[
          Text('Welcome to SparkClub!\nCurrently, this page has not been implemented, so please be patient and hopefully it will be finished soon.', textAlign: TextAlign.center),
        ],
      ),
    );
  }
}