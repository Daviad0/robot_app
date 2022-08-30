import 'package:flutter/material.dart';
import 'package:sparkclub/backend.dart';
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
    final List<BaseItem> items = TempBackend().getLandingItems();
    final List<BaseSubgroup> subgroups = TempBackend().getSubgroups();

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
                          onPressed: () => items[index].openLink(context),
                          child: const Text('Delete')
                        );
                      final Widget trailingWidget = items[index].link == null ? deleteButton : Row(
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
                          title: Text(items[index].name),
                          subtitle: items[index].getContent != null ? Text(items[index].getContent) : null,
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
                          title: Text(subgroups[index].name),
                          subtitle: Text(subgroups[index].getText),
                          leading: const Icon(Icons.group),
                          trailing: const Icon(Icons.chevron_right),
                          onTap: () => Navigator.of(context).push(
                            MaterialPageRoute(builder: (ctx) => Subgroup(name: subgroups[index].name, tag: subgroups[index].tag, role: subgroups[index].role)),
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