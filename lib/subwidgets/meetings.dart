import 'package:flutter/material.dart';
import 'package:sparkclub/backend.dart';
import 'package:sparkclub/buildables/singlemeeting.dart';
import 'package:sparkclub/constants.dart';

class Meetings extends StatefulWidget {
  const Meetings({Key? key}) : super(key: key);

  @override
  State<Meetings> createState() => _MeetingsState();
}

class _MeetingsState extends State<Meetings> {
  @override
  Widget build(BuildContext context) {
    final meetings = TempBackend().getMeetings();
    final upcomingMeetings = meetings[0];
    final pastMeetings = meetings[1];

    return SingleChildScrollView(
      child: Center(
        child: Column(
          children: <Widget>[
            const SizedBox(height: 32),
            Text('Upcoming Meetings', style: TextStyle(fontSize: 32, foreground: Paint()..color = Constants.textColor)),
            ListView.separated(
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 32),
                  child: Material(
                    elevation: 4,
                    child: ListTile(
                      title: Text(upcomingMeetings[index].name),
                      subtitle: Text(upcomingMeetings[index].time),
                      onTap: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => SingleMeeting(
                              meeting: upcomingMeetings[index],
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                );
              },
              separatorBuilder: (context, i) => const Divider(),
              itemCount: upcomingMeetings.length,
              shrinkWrap: true,
            ),
            const SizedBox(height: 32),
            Text('Past Meetings', style: TextStyle(fontSize: 32, foreground: Paint()..color = Constants.textColor)),
            ListView.separated(
              itemBuilder: (context, index) {
                return Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 32),
                  child: Material(
                    elevation: 4,
                    child: ListTile(
                      title: Text(pastMeetings[index].name),
                      subtitle: Text(pastMeetings[index].time),
                      onTap: () {
                        Navigator.of(context).push(
                          MaterialPageRoute(
                            builder: (context) => SingleMeeting(
                              meeting: pastMeetings[index],
                            ),
                          ),
                        );
                      },
                    ),
                  ),
                );
              },
              separatorBuilder: (context, i) => const Divider(),
              itemCount: pastMeetings.length,
              shrinkWrap: true,
            ),
          ],
        ),
      ),
    );
  }
}