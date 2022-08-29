import 'package:flutter/material.dart';
import 'package:sparkclub/buildables/subgroup.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  State<HomePage> createState() => HomePageState();
}

class HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        children: <Widget>[
          Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              children: <Widget>[
                Text('Active Items', textAlign: TextAlign.center, style: TextStyle(fontSize: 28, foreground: Paint()..color = Colors.indigo.shade800)),
                const SizedBox(height: 16),
              ],
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(32),
            child: Column(
              children: <Widget>[
                Text('My Subgroups', textAlign: TextAlign.center, style: TextStyle(fontSize: 28, foreground: Paint()..color = Colors.indigo.shade800)),
                const SizedBox(height: 16),
                // TODO: change this to a listbuilder of some sort
                // TODO: make listtiles roudned
                // Placeholder subgroup waiting for backend
                Material(
                  elevation: 10.0,
                  shadowColor: Colors.blueGrey,
                  child: ListTile(
                    title: const Text('Subgroup 1'),
                    subtitle: const Text('Subgroup Admin'),
                    leading: const Icon(Icons.group),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () => Navigator.of(context).push(
                      MaterialPageRoute(builder: (ctx) => const Subgroup(name: 'Subgroup 1', tag: 'SUB1', role: 'Admin')),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}