import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:sparkclub/constants.dart';
import 'package:sparkclub/homescreen.dart';
import 'package:sparkclub/signin.dart';

class Signup extends StatefulWidget {
  const Signup({Key? key}) : super(key: key);

  @override
  State<Signup> createState() => _SignupState();
}

class _SignupState extends State<Signup> {
  late TextEditingController _emailController;
  late TextEditingController _nameController;
  late TextEditingController _idController;
  late TextEditingController _usernameController;
  late TextEditingController _passwordController;

  bool _validateEmail = false;
  bool _validateName = false;
  bool _validateID = false;
  bool _validateUsername = false;
  bool _validatePassword = false;

  bool _hidingPassword = true;

  @override
  void initState() {
    super.initState();
    _emailController = TextEditingController();
    _nameController = TextEditingController();
    _idController = TextEditingController();
    _usernameController = TextEditingController();
    _passwordController = TextEditingController();
  }

  @override
  void dispose() {
    _emailController.dispose();
    _nameController.dispose();
    _idController.dispose();
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SingleChildScrollView(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Image.asset('../assets/lightning.png'),
              const SizedBox(height: 8),
              const Text('Sign Up', style: TextStyle(fontSize: 28)),
              const SizedBox(height: 8),
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
                child: TextField(
                  decoration: InputDecoration(
                    border: const OutlineInputBorder(),
                    icon: const Icon(Icons.email),
                    labelText: 'Email',
                    errorText: _validateEmail ? 'This field is required!' : null,
                  ),
                  onChanged: (value) => _validateEmail == true ? setState(() => _validateEmail = false) : null,
                  controller: _emailController,
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
                child: TextField(
                  decoration: InputDecoration(
                    border: const OutlineInputBorder(),
                    icon: const Icon(Icons.edit_outlined),
                    labelText: 'Full Name',
                    errorText: _validateName ? 'This field is required!' : null,
                  ),
                  onChanged: (value) => _validateName == true ? setState(() => _validateName = false) : null,
                  controller: _nameController,
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
                child: TextField(
                  decoration: InputDecoration(
                    border: const OutlineInputBorder(),
                    icon: const Icon(Icons.badge_outlined),
                    labelText: 'Student ID',
                    errorText: _validateID ? 'This field is required!' : null,
                  ),
                  onChanged: (value) => _validateID == true ? setState(() => _validateID = false) : null,
                  controller: _idController,
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
                child: TextField(
                  decoration: InputDecoration(
                    border: const OutlineInputBorder(),
                    icon: const Icon(Icons.person),
                    labelText: 'Username',
                    errorText: _validateUsername ? 'This field is required!' : null,
                  ),
                  onChanged: (value) => _validateUsername == true ? setState(() => _validateUsername = false) : null,
                  controller: _usernameController,
                ),
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Expanded(
                    child: Padding(
                      padding: const EdgeInsets.fromLTRB(8, 4, 4, 8),
                      child: TextField(
                        decoration: InputDecoration(
                          icon: const Icon(Icons.lock),
                          border: const OutlineInputBorder(),
                          labelText: 'Password',
                          errorText: _validatePassword ? 'This field is required!' : null,
                        ),
                        onChanged: (value) => _validatePassword == true ? setState(() => _validatePassword = false) : null,
                        // onEditingComplete: () => _passwordController.text.isEmpty ? setState(() => _validatePassword = true) : null, // DOES NOT WORK
                        controller: _passwordController,
                        obscureText: _hidingPassword,
                      ),
                    ),
                  ),
                  Padding(
                    padding: const EdgeInsets.fromLTRB(4, 8, 8, 8),
                    child: IconButton(
                      icon: Icon(_hidingPassword ? Icons.visibility_off : Icons.visibility), // I have no idea why these icons are switched
                      onPressed: () => setState(() => _hidingPassword = !_hidingPassword),
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8),
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
                      if (_emailController.text.isEmpty) { setState(() => _validateEmail = true); }
                      if (_nameController.text.isEmpty) { setState(() => _validateName = true); }
                      if (_idController.text.isEmpty) { setState(() => _validateID = true); }
                      if (_usernameController.text.isEmpty) { setState(() => _validateUsername = true); }
                      if (_passwordController.text.isEmpty) { setState(() => _validatePassword = true); }
                      if (
                        _validateEmail ||
                        _validateName ||
                        _validateID ||
                        _validateUsername ||
                        _validatePassword
                      ) { return; }
      
                      () async {
                        SharedPreferences prefs = await SharedPreferences.getInstance();
                        prefs.setString(StorageConstants.usernameKey, _usernameController.text);
                      }();
      
                      Navigator.of(context).pushReplacement(
                        MaterialPageRoute(builder: (ctx) => const MainWidget()),
                      );
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(content: Text('Signup has not been fully implemented yet, so you have been sent to the home screen without authentication.'))
                      );
                    },
                    child: const Text('Create'),
                  ),
                  const SizedBox(width: 8),
                  ElevatedButton(
                    style: ElevatedButton.styleFrom(
                      primary: Theme.of(context).colorScheme.secondary,
                      onPrimary: Theme.of(context).colorScheme.onSecondary,
                    ),
                    onPressed: () {
                      Navigator.of(context).pushReplacement(
                        PageRouteBuilder(
                          pageBuilder: (ctx, animation1, animation2) => const SignIn(),
                          transitionDuration: Duration.zero,
                          reverseTransitionDuration: Duration.zero
                        ),
                      );
                    },
                    child: const Text('Back')
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}