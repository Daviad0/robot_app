import 'package:flutter/material.dart';
import 'package:sparkclub/constants.dart';

class MyAccount extends StatelessWidget {
  const MyAccount({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    String username = 'quackings';
    String name = 'Kyle Rush';
    String email = 'kyle@quackings.com';
    String rank = 'ADMIN';
    Color rankColor = Colors.redAccent.shade700;
    int subgroupCount = 1;
    List<String> flags = ['*', 'ADMIN_REPRESENTATIVE', 'ADMIN_SUBGROUPS_MANAGER'];

    return Scaffold(
      appBar: AppBar(
        title: const Text('My Account'),
      ),
      body: Center(
        child: Column(
          children: <Widget>[
            const SizedBox(height: 16),
            const Padding(
              padding: EdgeInsets.all(16),
              child: Text('Hey there, ', style: TextStyle(fontSize: 24)), // TODO: add random strings (maybe time of day)
            ),
            const SizedBox(height: 8),
            Text(username, style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, foreground: Paint()..color = Constants.textColor)),
            const SizedBox(height: 12),
            Padding(
              padding: const EdgeInsets.all(16),
              child: Container(
                decoration: BoxDecoration(
                  color: rankColor,
                  borderRadius: BorderRadius.circular(16),
                  // TODO: shadow looks wonkys
                  boxShadow: [
                    BoxShadow(
                      color: Colors.grey.withOpacity(0.5),
                      spreadRadius: 4,
                      blurRadius: 7,
                      offset: const Offset(0, 4),
                    ),
                  ],
                ),
                padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 20),
                child: Text(rank, style: TextStyle(fontSize: 24, foreground: Paint()..color = Colors.white)),
              ),
            ),
            const SizedBox(height: 16),
            Material(
              elevation: 20.0,
              borderRadius: BorderRadius.circular(8),
              child: Container(
                padding: const EdgeInsets.all(16),
                child: Column(
                  children: <Widget>[
                    Text(name, style: const TextStyle(fontSize: 16)),
                    const SizedBox(height: 16),
                    Text(email, style: const TextStyle(fontSize: 16)),
                    const SizedBox(height: 16),
                    Text("In $subgroupCount subgroup${subgroupCount == 1 ? '' : 's'}", style: const TextStyle(fontSize: 16)),
                    const SizedBox(height: 16),
                    Text(flags.join(','), style: const TextStyle(fontSize: 12)),
                  ],
                ),
              ),
            ),
          ],
        ),
      )
    );
  }
}