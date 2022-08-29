import 'package:flutter/material.dart';
import 'package:sparkclub/subwidgets/home.dart';
import 'package:sparkclub/subwidgets/unfinished.dart';

class Finder {
  static Widget? find(int navIndex) => navIndex == 0 ? const HomePage() : const Unfinished();
}