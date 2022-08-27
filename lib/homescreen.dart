import 'package:flutter/material.dart';
import 'package:sparkclub/constants.dart';
import 'package:sparkclub/subwidgets/finder.dart';

class MainWidget extends StatefulWidget {
  const MainWidget({Key? key}) : super(key: key);

  @override
  State<MainWidget> createState() => _MainWidgetState();
}

class _MainWidgetState extends State<MainWidget> {
  int _navigationBarIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text(Constants.appTitle),
        leading: Padding(
          padding: const EdgeInsets.all(2),
          child: Image.asset('../assets/sparkclub.png'),
        ),
        actions: <Widget>[
          PopupMenuButton<int>(
            itemBuilder: (context) => Constants.popupMenuItems,
            onSelected: (item) => _handlePopupMenu(context, item),
          ),
        ],
      ),
      body: _getCurrentNavWidget(),
      bottomNavigationBar: BottomNavigationBar(
        items: Constants.bottomNavItems,
        currentIndex: _navigationBarIndex,
        selectedItemColor: Theme.of(context).colorScheme.onPrimary,
        unselectedItemColor: Theme.of(context).colorScheme.onPrimary.withOpacity(0.35),
        backgroundColor: Theme.of(context).colorScheme.primary,
        onTap: (index) {
          setState(() => _navigationBarIndex = index);
        },
      ),
    );
  }

  Widget _getCurrentNavWidget() => Finder.find(_navigationBarIndex)!;
  void _handlePopupMenu(BuildContext context, int value) => FunctionConstants.popupMenuFunctions[value](context);
}