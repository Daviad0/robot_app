import 'package:flutter/material.dart';

class Meetings extends StatefulWidget {
  const Meetings({Key? key}) : super(key: key);

  @override
  State<Meetings> createState() => MeetingsState();
}

class MeetingsState extends State<Meetings> {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        children: const <Widget>[
          Text('Currently unfinished.'),
        ],
      ),
    );
  }
}