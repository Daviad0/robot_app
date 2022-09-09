import 'package:flutter/material.dart';
import 'package:sparkclub/constants.dart';
import 'package:sparkclub/signin.dart';

class IDSignIn extends StatefulWidget {
  const IDSignIn({Key? key}) : super(key: key);

  @override
  State<IDSignIn> createState() => _IDSignInState();
}

class _IDSignInState extends State<IDSignIn> {
  late TextEditingController _idController;

  bool _validateField = false;

  @override
  void initState() {
    super.initState();
    _idController = TextEditingController();
  }

  @override
  void dispose() {
    _idController.dispose();
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
            const SizedBox(height: 8),
            const Text('Student ID Login', style: TextStyle(fontSize: 28), textAlign: TextAlign.center),
            const SizedBox(height: 8),
            const Text('If you do not want to login with your email,\nyou may login with your student ID. Your \nstudent ID is linked to your account.', textAlign: TextAlign.center),
            const SizedBox(height: 16),
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: TextField(
                decoration: InputDecoration(
                  border: const OutlineInputBorder(),
                  icon: const Icon(Icons.person),
                  hintText: 'Student ID',
                  errorText: _validateField ? 'This field is required!' : null,
                ),
                controller: _idController,
                onChanged: (value) => _validateField == true ? setState(() => _validateField = false) : null,
              ),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              mainAxisSize: MainAxisSize.max,
              children: <Widget>[
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    primary: Theme.of(context).colorScheme.primary,
                    onPrimary: Theme.of(context).colorScheme.onPrimary,
                  ),
                  onPressed: () {
                    if (_idController.text.isEmpty) { setState(() => _validateField = true); }
                    if (_validateField) { return; }

                    FunctionConstants.showUnfinishedSnackbar(context);
                  },
                  child: const Text('Sign In'),
                ),
                const SizedBox(width: 8),
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
              ],
            ),
          ]
        ),
      ),
    );
  }
}