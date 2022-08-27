import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sparkclub/constants.dart';
import 'package:sparkclub/homescreen.dart';

class SignIn extends StatefulWidget {
  const SignIn({Key? key}) : super(key: key);

  @override
  State<SignIn> createState() => _SignInState();
}

class _SignInState extends State<SignIn> {
  late TextEditingController _usernameController;
  late TextEditingController _passwordController;

  bool _validateUsername = false;
  bool _validatePassword = false;

  @override
  void initState() {
    super.initState();
    _usernameController = TextEditingController();
    _passwordController = TextEditingController();
  }

  @override
  void dispose() {
    _usernameController.dispose();
    _passwordController.dispose();
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
            const Text('Currently, signin has not been implemented, so you may enter anything into the fields and you will be directed to the home screen.', style: TextStyle(fontSize: 16), textAlign: TextAlign.center),
            const SizedBox(height: 16),
            Padding(
              padding: const EdgeInsets.all(8),
              child: TextField(
                decoration: InputDecoration(
                  border: const OutlineInputBorder(),
                  labelText: 'Username',
                  errorText: _validateUsername ? 'This field is required!' : null,
                ),
                onChanged: (value) => _validateUsername == true ? setState(() => _validateUsername = false) : null,
                // onEditingComplete: () => _usernameController.text.isEmpty ? setState(() => _validateUsername = true) : null, // DOES NOT WORK
                controller: _usernameController,
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(8),
              child: TextField(
                decoration: InputDecoration(
                  border: const OutlineInputBorder(),
                  labelText: 'Password',
                  errorText: _validatePassword ? 'This field is required!' : null,
                ),
                onChanged: (value) => _validatePassword == true ? setState(() => _validatePassword = false) : null,
                // onEditingComplete: () => _passwordController.text.isEmpty ? setState(() => _validatePassword = true) : null, // DOES NOT WORK
                controller: _passwordController,
                obscureText: true,
              ),
            ),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    primary: Theme.of(context).colorScheme.primary,
                    onPrimary: Theme.of(context).colorScheme.onPrimary,
                  ),
                  onPressed: () {
                    if (_usernameController.text.isEmpty) { setState(() => _validateUsername = true); }
                    if (_passwordController.text.isEmpty) { setState(() => _validatePassword = true); }
                    if (_validateUsername || _validatePassword) { return; }

                    // TODO: fix textfields being laggy (due to setState() being called a lot)
                    // TODO: implement http request to signin, for now just send user to home screen
                    () async {
                      SharedPreferences prefs = await SharedPreferences.getInstance();
                      prefs.setString(StorageConstants.usernameKey, _usernameController.text);
                    }();
                    Navigator.of(context).pushReplacement(
                      MaterialPageRoute(builder: (ctx) => const MainWidget()),
                    );
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(content: Text('Signin has not been fully implemented yet, so you have been sent to the home screen without authentication.'))
                    );
                  },
                  child: const Text('Sign In'),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  style: ElevatedButton.styleFrom(
                    primary: Theme.of(context).colorScheme.secondary,
                    onPrimary: Theme.of(context).colorScheme.onSecondary,
                  ),
                  onPressed: () {},
                  child: const Text('Forgot Password?'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}