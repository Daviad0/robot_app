import 'package:flutter/material.dart';
import 'package:sparkclub/signin.dart';

class AlternateSignIn extends StatefulWidget {
  const AlternateSignIn({Key? key}) : super(key: key);

  @override
  State<AlternateSignIn> createState() => _AlternateSignInState();
}

class _AlternateSignInState extends State<AlternateSignIn> {
  late TextEditingController _emailController;
  late TextEditingController _codeController;

  bool _codeFieldEnabled = false;

  @override
  void initState() {
    super.initState();
    _emailController = TextEditingController();
    _codeController = TextEditingController();
  }

  @override
  void dispose() {
    _emailController.dispose();
    _codeController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            Image.asset('../assets/lightning.png'),
            Text('Temporary Login', style: TextStyle(fontSize: 32, foreground: Paint()..color = Colors.indigo.shade800), textAlign: TextAlign.center),
            const SizedBox(height: 16),
            Row(
              children: <Widget>[
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.fromLTRB(8, 8, 4, 8),
                    child: TextField(
                      decoration: const InputDecoration(
                        icon: Icon(Icons.email),
                        border: OutlineInputBorder(),
                        labelText: 'Email',
                      ),
                      controller: _emailController,
                    ),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(4, 8, 8, 8),
                  child: ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      primary: Theme.of(context).colorScheme.primary,
                      onPrimary: Theme.of(context).colorScheme.onPrimary,
                    ),
                    onPressed: () {
                      ScaffoldMessenger.of(context).clearSnackBars();
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: const Text('Sorry, Email login has not been implemented yet!'),
                          backgroundColor: Theme.of(context).colorScheme.error,
                        )
                      );
                    },
                    child: const Text('Send Code'),
                  ),
                ),
              ],
            ),
            Padding(
              padding: const EdgeInsets.all(8),
              child: TextField(
                decoration: const InputDecoration(
                  icon: Icon(Icons.vpn_key),
                  border: OutlineInputBorder(),
                  labelText: 'Code',
                ),
                controller: _codeController,
                enabled: _codeFieldEnabled,
              ),
            ),
            const SizedBox(height: 8),
            ElevatedButton(
              style: ElevatedButton.styleFrom(
                primary: Theme.of(context).colorScheme.secondary,
                onPrimary: Theme.of(context).colorScheme.onSecondary,
              ),
              onPressed: () => Navigator.of(context).pushReplacement(
                PageRouteBuilder(
                  pageBuilder: (ctx, animation1, animation2) => const SignIn(),
                  transitionDuration: Duration.zero,
                  reverseTransitionDuration: Duration.zero
                ),
              ),
              child: const Text('Back'),
            ),
          ]
        ),
      ),
    );
  }
}