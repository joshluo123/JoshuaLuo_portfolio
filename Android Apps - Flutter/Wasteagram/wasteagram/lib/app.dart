import 'package:flutter/material.dart';
import 'screens/list_screen.dart';
import 'screens/new_post_screen.dart';
import 'screens/detail_screen.dart';


class App extends StatelessWidget {
  const App({ Key? key }) : super(key: key);

  static final screenRoutes = {
    '/': (context) => const ListScreen(),
    'view_post': (context) => const DetailScreen(),
    'new_post': (context) => const NewPostScreen()
  };

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CS 492 Project 5 - Joshua Luo: Wasteagram',
      theme: ThemeData.dark(),
      routes: screenRoutes,
    );
  }
}