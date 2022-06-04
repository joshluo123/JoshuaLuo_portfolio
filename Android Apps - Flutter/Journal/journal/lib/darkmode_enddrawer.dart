import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';


class DarkModeEnddrawer extends StatefulWidget {

  final void Function(bool) changeTheme;
  final SharedPreferences preferences;

  const DarkModeEnddrawer({ Key? key, required this.changeTheme, required this.preferences }) : super(key: key);

  @override
  State<DarkModeEnddrawer> createState() => DarkModeEnddrawerState();
}

class DarkModeEnddrawerState extends State<DarkModeEnddrawer> {

  late bool toggled;

  @override
  void initState() {
    super.initState();
    toggled = widget.preferences.getBool('dark mode') as bool;
  }

  @override
  Widget build(BuildContext context) {
    return Drawer(
      child: ListView(
        children: [
          DrawerHeader(
            decoration: const BoxDecoration(
              color: Colors.blue
            ),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: const[
                Text(
                  'Settings',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 40
                  )
                )
              ]
            )
          ),
          SwitchListTile(
            title: const Text('Dark Mode'),
            secondary: const Icon(Icons.dark_mode),
            subtitle: const Text('Toggle dark mode theme'),
            value: toggled,
            onChanged: (bool value) {
              widget.changeTheme(value);
              setState(() => toggled = value);
            },
          )
        ]
      )
    );
  }
}