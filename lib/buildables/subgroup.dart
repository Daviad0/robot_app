import 'package:flutter/material.dart';
import 'package:sparkclub/backend.dart';
import 'package:sparkclub/constants.dart';

class Subgroup extends StatefulWidget {
  const Subgroup({Key? key, required this.name, required this.tag, required this.role}) : super(key: key);

  final String name;
  final String tag;
  final String? role;

  @override
  State<Subgroup> createState() => _SubgroupState();
}

class _SubgroupState extends State<Subgroup> {
  @override
  Widget build(BuildContext context) {
    final BaseSubgroup subgroup = TempBackend().getSubgroup(widget.name, widget.tag);

    return Scaffold(
      appBar: AppBar(
        title: Text(widget.name),
      ),
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            children: <Widget>[
              const SizedBox(height: 32),
              Text(widget.name, style: TextStyle(fontSize: 32, foreground: Paint()..color = Constants.textColor)),
              const SizedBox(height: 32),
              Container(
                decoration: BoxDecoration(
                  color: Colors.indigo.shade900,
                ),
                padding: const EdgeInsets.all(12),
                child: Text('• ${widget.tag}', style: TextStyle(fontSize: 16, foreground: Paint()..color = Colors.white)),
              ),
              const SizedBox(height: 32),
              Text(widget.role != null ? 'Your role in this subgroup is: ${widget.role}' : 'You are not a member of this subgroup.'),
              const SizedBox(height: 32),
              Column(
                children: <Widget>[
                  Text('Subgroup Items', style: TextStyle(fontSize: 24, foreground: Paint()..color = Constants.textColor)),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      primary: Theme.of(context).colorScheme.primary,
                      onPrimary: Theme.of(context).colorScheme.onPrimary,
                    ),
                    onPressed: () => FunctionConstants.showUnfinishedSnackbar(context),
                    child: const Text('Add Item'),
                  ),
                  ListView.separated(
                    itemCount: subgroup.items.length,
                    itemBuilder: (BuildContext context, int index) {
                      final Widget deleteButton = TextButton(
                          style: TextButton.styleFrom(
                            primary: Theme.of(context).colorScheme.error,
                          ),
                          onPressed: () => subgroup.items[index].openLink(context),
                          child: const Text('Delete')
                        );
                      final Widget trailingWidget = subgroup.items[index].link == null ? deleteButton : Row(
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
    
                      return Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 32),
                        child: Material(
                          elevation: 4,
                          shadowColor: Colors.blueGrey,
                          child: ListTile(
                            title: Text(subgroup.items[index].name),
                            subtitle: subgroup.items[index].getContent != null ? Text(subgroup.items[index].getContent) : null,
                            trailing: trailingWidget
                          ),
                        ),
                      );
                    },
                    separatorBuilder: (ctx, index) => const Divider(),
                    shrinkWrap: true,
                  ),
                ],
              ),
              const SizedBox(height: 32),
              Column(
                children: <Widget>[
                  Text('Upcoming Meetings', style: TextStyle(fontSize: 24, foreground: Paint()..color = Constants.textColor)),
                  const SizedBox(height: 16),
                  ListView.separated(
                    itemBuilder: (ctx, index) {
                      return Padding(
                        padding: const EdgeInsets.symmetric(horizontal: 32),
                        child: Material(
                          elevation: 20.0,
                          borderRadius: BorderRadius.circular(8),
                          child: Container(
                            padding: const EdgeInsets.all(16),
                            child: Column(
                              children: <Widget>[
                                Text(subgroup.meetings[index].time, style: const TextStyle(fontSize: 18)),
                                const SizedBox(height: 16),
                                Text(subgroup.meetings[index].name, style: const TextStyle(fontStyle: FontStyle.italic)),
                              ],
                            ),
                          ),
                        ),
                      );
                    },
                    separatorBuilder: (ctx, index) => const Divider(),
                    itemCount: subgroup.meetings.length,
                    shrinkWrap: true,
                  ),
                ],
              ),
              const SizedBox(height: 32),
              Column(
                children: <Widget>[
                  Text('Members', style: TextStyle(fontSize: 24, foreground: Paint()..color = Constants.textColor)),
                  const SizedBox(height: 16),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      primary: Theme.of(context).colorScheme.primary,
                      onPrimary: Theme.of(context).colorScheme.onPrimary,
                    ),
                    onPressed: () => FunctionConstants.showUnfinishedSnackbar(context),
                    child: const Text('Add Member'),
                  ),
                  const SizedBox(height: 16),
                  GridView.count(
                    crossAxisCount: 2,
                    crossAxisSpacing: 16,
                    mainAxisSpacing: 8,
                    childAspectRatio: 5,
                    shrinkWrap: true,
                    children: List.generate(subgroup.members.length, (index) {
                      return Center(
                        child: Padding(
                          padding: const EdgeInsets.all(8),
                          child: Material(
                            elevation: 4,
                            borderRadius: BorderRadius.circular(32),
                            child: Container(
                              padding: const EdgeInsets.all(8),
                              height: double.infinity,
                              width: double.infinity,
                              child: Center(child: Text(subgroup.members[index], textAlign: TextAlign.center, style: const TextStyle(fontSize: 20))),
                            ),
                          ),
                        ),
                      );
                    }),
                  ),
                ],
              ),
              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }
}