import 'package:flutter/material.dart';
import 'package:sparkclub/constants.dart';

enum LoadItems {
  landingPage,
  meetings,
  subgroup,
  individualMeeting,
  account,
  settings,
}

// TODO: make all base classes null safe
class BaseItem {
  BaseItem({
    required this.name,
    this.content,
    this.link,
  });

  String name;
  String? content;
  String? link;

  dynamic get getContent => content == null ? null : content!;
  dynamic get getLink => link == null ? null : link!;

  void openLink(BuildContext context) {
    if (link == null) return;
    FunctionConstants.showUnfinishedSnackbar(context);
  }
}

class BaseMeeting {
  BaseMeeting({
    required this.name,
    this.time = '',
    this.description = '',
    this.hasPast = false,
    this.membersAttending = const [],
  });

  String name;
  String description;
  String time;
  bool hasPast;
  List<String> membersAttending;
}

// TODO: maybe add an add() method for meetings, members, and items
class BaseSubgroup {
  BaseSubgroup({
    required this.name,
    required this.tag,
    this.role,
    this.text,
    this.items = const [],
    this.meetings = const [],
    this.members = const [],
  });

  String name;
  String tag;
  String? role;
  String? text;
  List<BaseItem> items;
  List<BaseMeeting> meetings;
  List<String> members;

  dynamic get getText => text == null ? null : text!;

  set setItems(List<BaseItem> items) => this.items = items;
  set setMeetings(List<BaseMeeting> meetings) => this.meetings = meetings;
  set setMembers(List<String> members) => this.members = members;
}

abstract class BackendFuncs {
  // May return another value/future
  void alternateSignin(String email);
  List<BaseItem> getLandingItems();
  BaseSubgroup getSubgroup(String name, String tag, [String? role]);
  List<BaseSubgroup> getSubgroups();
  List<List<BaseMeeting>> getMeetings();
  void load(LoadItems item, {Map<String, dynamic>? args});
  void signin(String username, String password);
}

// Used for testing and gives mock values to widgets
class TempBackend extends BackendFuncs {
  @override
  void alternateSignin(String email) => throw UnimplementedError();

  @override
  BaseSubgroup getSubgroup(String name, String tag, [String? role]) {
    List<BaseItem> items = [
      BaseItem(
        name: 'Item 1',
        content: 'This is item 1',
        link: 'https://www.google.com',
      ),
      BaseItem(
        name: 'Item 2',
        content: 'This is item 2',
        link: 'https://www.google.com',
      ),
      BaseItem(
        name: 'Item 3',
        content: 'This is item 3',
        link: 'https://www.google.com',
      ),
    ];
    dynamic upcomingMeetings = [
      {
        'name': 'Rookie Informational Meeting',
        'time': '9/7 at 2:30 PM',
      }
    ];
    final List<String> members = [
      'David',
      'David',
      'David',
      'David',
      'Kyle',
    ];
    upcomingMeetings = List.generate(upcomingMeetings.length, (index) {
      return BaseMeeting(name: upcomingMeetings[index]['name'], time: upcomingMeetings[index]['time']);
    });
    return BaseSubgroup(name: name, tag: tag, role: role, items: items, meetings: upcomingMeetings, members: members);
  }

  @override
  void load(LoadItems item, {Map<String, dynamic>? args}) => throw UnimplementedError();

  @override
  void signin(String username, String password) => throw UnimplementedError();
  
  @override
  List<BaseSubgroup> getSubgroups() {
    final List<Map<String, dynamic>> tempSubgroups = [
      {
        'name': 'Subgroup 1',
        'text': 'Subgroup Admin',
        'rank': 'Admin',
        'tag': 'SUB1',
      },
      {
        'name': 'Subgroup 2',
        'text': 'Not involved',
        'rank': null,
        'tag': 'SUB2',
      },
    ];
    return List.generate(tempSubgroups.length, (index) {
      return BaseSubgroup(
        name: tempSubgroups[index]['name'],
        tag: tempSubgroups[index]['tag'],
        role: tempSubgroups[index]['rank'],
        text: tempSubgroups[index]['text'],
      );
    });
  }
  
  @override
  List<BaseItem> getLandingItems() {
    final List<Map<String, dynamic>> tempItems = [
      {
        'name': 'Test Item',
        'content': 'This is content',
        'link': 'http://quackings.com',
      },
      {
        'name': 'Test Item without link',
        'content': 'This is content, this also doesnt have a link attached so the button will not show. This is also testing for overflow: WOW! This is a lot of overflow, I hope the ListTile object can handle it.',
        'link': null,
      },
    ];
    return List.generate(tempItems.length, (index) {
      return BaseItem(
        name: tempItems[index]['name'],
        content: tempItems[index]['content'],
        link: tempItems[index]['link'],
      );
    });
  }
  
  @override
  List<List<BaseMeeting>> getMeetings() {
    final List<Map<String, dynamic>> tempMeetings = [
      {
        'name': 'Meeting',
        'time': '9/7 at 2:30 PM',
        'description': 'this is a meeting no way!',
        'hasPast': false,
      },
      {
        'name': 'Meeting 0',
        'time': '9/7 at 2:30 PM',
        'description': 'this is a meeting no way!',
        'hasPast': false,
      },
      {
        'name': 'Meeting 1',
        'time': '9/7 at 2:30 PM',
        'description': 'this is a meeting no way!',
        'hasPast': true,
      },
      {
        'name': 'Meeting 2',
        'time': '9/7 at 2:30 PM',
        'description': 'this is a meeting no way!',
        'hasPast': true,
      },
      {
        'name': 'Meeting 3',
        'time': '9/7 at 2:30 PM',
        'description': 'this is a meeting no way!',
        'hasPast': true,
      },
      {
        'name': 'Meeting 4',
        'time': '9/7 at 2:30 PM',
        'description': 'this is a meeting no way!',
        'hasPast': true,
      },
    ];
    final allItems = List.generate(tempMeetings.length, (index) {
      return BaseMeeting(name: tempMeetings[index]['name'], time: tempMeetings[index]['time'], description: tempMeetings[index]['description'], hasPast: tempMeetings[index]['hasPast']);
    });
    final pastItems = allItems.where((meeting) => meeting.hasPast).toList();
    final upcomingItems = allItems.where((meeting) => !meeting.hasPast).toList();
    return [upcomingItems, pastItems];
  }
}