import 'package:flutter/material.dart';

class Subgroup extends StatefulWidget {
  const Subgroup({Key? key, required this.name, required this.tag, required this.role}) : super(key: key);

  final String name;
  final String tag;
  final String role;

  @override
  State<Subgroup> createState() => _SubgroupState();
}

class _SubgroupState extends State<Subgroup> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.name),
      ),
      body: Center(
        child: Column(
          children: <Widget>[
            Padding(
              padding: const EdgeInsets.all(32),
              child: Text(widget.name, style: TextStyle(fontSize: 32, foreground: Paint()..color = Colors.indigo.shade900)),
            ),
            Padding(
              padding: const EdgeInsets.all(32),
              child: Container(
                decoration: BoxDecoration(
                  color: Colors.indigo.shade900,
                ),
                padding: const EdgeInsets.all(12),
                child: Text('• ${widget.tag}', style: TextStyle(fontSize: 16, foreground: Paint()..color = Colors.white)),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(16),
              child: Text('Your role in this subgroup is: ${widget.role}'),
            ),
            Padding(
              padding: const EdgeInsets.all(32),
              child: Text('Subgroup Items', style: TextStyle(fontSize: 24, foreground: Paint()..color = Colors.indigo.shade900)),
            ),
            const SizedBox(height: 16,),
            Padding(
              padding: const EdgeInsets.all(32),
              child: Text('Upcoming Meetings', style: TextStyle(fontSize: 24, foreground: Paint()..color = Colors.indigo.shade900)),
            ),
            const SizedBox(height: 16,),
            Padding(
              padding: const EdgeInsets.all(32),
              child: Text('Members', style: TextStyle(fontSize: 24, foreground: Paint()..color = Colors.indigo.shade900)),
            ),
            const SizedBox(height: 16,),
          ],
        ),
      ),
    );
  }
}