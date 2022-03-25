import 'package:flutter/material.dart';
import 'main_tab_controller.dart';

class App extends StatelessWidget {

  const App ({ Key? key }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CS 492 Project 3 - Joshua Luo',
      theme: ThemeData(primarySwatch: Colors.lightGreen, scaffoldBackgroundColor: Colors.blueGrey),
      home: MainTabController()
    );
  }
}