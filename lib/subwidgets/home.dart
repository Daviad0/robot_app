import 'package:flutter/material.dart';
import 'package:sparkclub/buildables/subgroup.dart';
import 'package:sparkclub/constants.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => HomePageState();
}

class HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    const List<Map<String, dynamic>> items = [
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
    const List<Map<String, dynamic>> subgroups = [
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

    return SingleChildScrollView(
      child: Center(
        child: Column(
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.all(32),
              child: Column(
                children: <Widget>[
                  Text('Active Items', textAlign: TextAlign.center, style: TextStyle(fontSize: 28, foreground: Paint()..color = Colors.indigo.shade800)),
                  const SizedBox(height: 12),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      primary: Theme.of(context).colorScheme.primary,
                      onPrimary: Theme.of(context).colorScheme.onPrimary,
                    ),
                    onPressed: () => FunctionConstants.showUnfinishedSnackbar(context),
                    child: const Text('New Item'),
                  ),
                  const SizedBox(height: 8),
                  ListView.separated(
                    itemCount: items.length,
                    itemBuilder: (BuildContext context, int index) {
                      final Widget deleteButton = TextButton(
                          style: TextButton.styleFrom(
                            primary: Theme.of(context).colorScheme.error,
                          ),
                          onPressed: () => FunctionConstants.showUnfinishedSnackbar(context),
                          child: const Text('Delete')
                        );
                      final Widget trailingWidget = items[index]['link'] == null || items[index]['link'] == '' ? deleteButton : Row(
                        mainAxisSize: MainAxisSize.min,
                        children: <Widget>[
                          TextButton(
                            style: TextButton.styleFrom(
                              primary: Theme.of(context).colorScheme.primary,
                            ),
                            onPressed: () => FunctionConstants.showUnfinishedSnackbar(context),
                            child: const Text('Open Link'),
                          ),
                          const SizedBox(width: 4),
                          deleteButton,
                        ],
                      );
    
                      return Material(
                        elevation: 4,
                        shadowColor: Colors.blueGrey,
                        child: ListTile(
                          title: Text(items[index]['name']),
                          subtitle: items[index]['content'] != null ? Text(items[index]['content']) : null,
                          trailing: trailingWidget
                        ),
                      );
                    },
                    separatorBuilder: (ctx, index) => const Divider(),
                    shrinkWrap: true,
                  ),
                ],
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(32),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: <Widget>[
                  Text('My Subgroups', textAlign: TextAlign.center, style: TextStyle(fontSize: 28, foreground: Paint()..color = Colors.indigo.shade800)),
                  const SizedBox(height: 16),
                  ListView.separated(
                    padding: const EdgeInsets.all(8),
                    itemCount: subgroups.length,
                    itemBuilder: (BuildContext context, int index) {
                      return Material(
                        elevation: 10.0,
                        shadowColor: Colors.blueGrey,
                        child: ListTile(
                          title: Text(subgroups[index]['name']),
                          subtitle: Text(subgroups[index]['text']),
                          leading: const Icon(Icons.group),
                          trailing: const Icon(Icons.chevron_right),
                          onTap: () => Navigator.of(context).push(
                            MaterialPageRoute(builder: (ctx) => Subgroup(name: subgroups[index]['name'], tag: subgroups[index]['tag'], role: subgroups[index]['rank'])),
                          ),
                        ),
                      );
                    },
                    separatorBuilder: (context, index) => const Divider(),
                    shrinkWrap: true,
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}