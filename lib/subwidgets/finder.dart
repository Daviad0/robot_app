import 'package:flutter/material.dart';
import 'package:sparkclub/popupwidgets/myaccount.dart';
import 'package:sparkclub/subwidgets/home.dart';

class Finder {
  static Widget? find(int navIndex) {
    switch (navIndex) {
      case 0:
      case 1:
        return const Home();
      default:
        return null;
    }
  }
}