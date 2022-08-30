import 'package:flutter/material.dart';
import 'package:sparkclub/backend.dart';
import 'package:sparkclub/constants.dart';

class SingleMeeting extends StatelessWidget {
  const SingleMeeting({
    Key? key,
    required this.meeting,
  }) : super(key: key);

  final BaseMeeting meeting;

  @override
  Widget build(BuildContext context) {
    final List<String> suffix = meeting.hasPast ? ['ed', 'attended!'] : ['ing', 'has attended yet!'];
    return Scaffold(
      appBar: AppBar(
        title: const Text('Individual Meeting'),
      ),
      body: Center(
        child: Column(
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.all(32),
              child: SizedBox(
                width: double.infinity,
                child: Material(
                  elevation: 10,
                  borderRadius: BorderRadius.circular(16),
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      children: <Widget>[
                        Text(meeting.name, style: TextStyle(fontSize: 32, foreground: Paint()..color = Constants.textColor)),
                        const SizedBox(height: 8),
                        Text(meeting.time, style: TextStyle(fontSize: 20, foreground: Paint()..color = Constants.textColor)),
                        const SizedBox(height: 16),
                        Text(meeting.description, style: TextStyle(fontSize: 16, foreground: Paint()..color = Constants.textColor)),
                        const SizedBox(height: 8),
                        Text(meeting.membersAttending.isNotEmpty ? "Attend${suffix[0]} members: ${meeting.membersAttending.join(', ')}" : 'Nobody ${suffix[1]}', style: TextStyle(fontSize: 16, foreground: Paint()..color = Constants.textColor)),
                      ],
                    ),
                  ),
                ),
              ),
            ),
            const SizedBox(height: 32),
            Text('Member Statuses', style: TextStyle(fontSize: 32, foreground: Paint()..color = Constants.textColor)),
          ],
        ),
      ),
    );
  }
}