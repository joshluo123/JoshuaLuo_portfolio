import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'screens/journal_screen.dart';
import 'screens/new_journal_entry_screen.dart';
import 'screens/view_journal_entry_screen.dart';


class App extends StatefulWidget {

  final SharedPreferences preferences;

  const App({ Key? key, required this.preferences }) : super(key: key);

  @override
  AppState createState() => AppState();
}

class AppState extends State<App> {

  late ThemeData theme;

  @override initState() {
    super.initState();
    initTheme();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CS 492 Project 4 - Joshua Luo: Journal',
      theme: theme,
      routes: {
        '/': (context) => JournalScreen(
          changeTheme: changeTheme,
          preferences: widget.preferences
        ),
        'view_je': (context) => ViewJournalEntryScreen(
          changeTheme: changeTheme,
          preferences: widget.preferences
        ),
        'new_je': (context) => NewJournalEntryScreen(
          changeTheme: changeTheme,
          preferences: widget.preferences
        )
      } 
    );
  }

  void initTheme() {
    bool? isDark = widget.preferences.getBool('dark mode');

    if (isDark == null) {
      widget.preferences.setBool('dark mode', false);
      theme = ThemeData.light();
    } else if (isDark) {
      theme = ThemeData.dark();
    } else {
      theme = ThemeData.light();
    }
  }

  void changeTheme(bool isDark) {
    widget.preferences.setBool('dark mode', isDark);

    if (isDark) {
      setState( () => theme = ThemeData.dark() );
    } else {
      setState( () => theme = ThemeData.light() );
    }
  }
}
