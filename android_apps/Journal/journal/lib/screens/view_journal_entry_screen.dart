import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:journal/journal_entry_details.dart';
import '../darkmode_enddrawer.dart';
import '../models/journal_entry.dart';


class ViewJournalEntryScreen extends StatelessWidget {

  final void Function(bool) changeTheme;
  final SharedPreferences preferences;

  const ViewJournalEntryScreen({ Key? key, required this.changeTheme, required this.preferences }) : super(key: key);

  @override
  Widget build(BuildContext context) {

    final JournalEntry receivedJournalEntry = ModalRoute.of(context)?.settings.arguments as JournalEntry;

    return Scaffold(
      appBar: AppBar(
        leading: const BackButton(),
        title: Center(
          child: Text(receivedJournalEntry.dateTime)
        ),
      ),
      endDrawer: DarkModeEnddrawer(
        changeTheme: changeTheme,
        preferences: preferences
      ),
      body: JournalEntryDetails(journalEntry: receivedJournalEntry)
    );
  }
}