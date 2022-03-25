import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:journal/journal_entry_details.dart';
import '../darkmode_enddrawer.dart';
import '../db/database_manager.dart';
import '../models/journal.dart';
import '../models/journal_entry.dart';


class JournalScreen extends StatefulWidget {

  final void Function(bool) changeTheme;
  final SharedPreferences preferences;

  const JournalScreen({ Key? key, required this.changeTheme, required this.preferences }) : super(key: key);

  @override
  JournalScreenState createState() => JournalScreenState();
}

class JournalScreenState extends State<JournalScreen> {
  
  static Widget journal = const Center(
    child: Text(
      'Loading...',
      style: TextStyle(
        fontSize: 30
      )
    )
  );
  static Widget journalEntryDetails = const Padding(
    padding: EdgeInsets.all(5),
    child: Center(
      child: Text(
        'Select a journal entry on the left to view its details'
      )
    )
  );

  @override
  void initState() {
    super.initState();
    loadJournalEntries();
  }
  
  void loadJournalEntries() async {
    final databaseManager = DatabaseManager.getInstance();
    List<JournalEntry> journalEntries = await databaseManager.getJournalEntries();
    setState( () {
      journal = Journal(entries: journalEntries, updateJourneyEntryDetails: updateJourneyEntryDetails);
    });
  }

  @override
  Widget build(BuildContext context) {
    if (MediaQuery.of(context).size.width < 700) {
      return portraitScaffold(context);
    } else {
      return landscapeScaffold(context);
    }
  }

  Widget portraitScaffold(BuildContext context) {
    return Scaffold(
      appBar: journalEntriesAppBar(),
      endDrawer: journalEntriesEnddrawer(),
      body: journal,
      floatingActionButton: addJournalEntryButton(),
    );
  }

  Widget landscapeScaffold(BuildContext context) {
    return Scaffold(
      appBar: journalEntriesAppBar(),
      endDrawer: journalEntriesEnddrawer(),
      body: Row(
        children: [
          SizedBox(
            height: MediaQuery.of(context).size.height,
            width: MediaQuery.of(context).size.width / 2,
            child: Padding(
              padding: const EdgeInsets.all(5),
              child: journal
            )
          ),
          SizedBox(
            height: MediaQuery.of(context).size.height,
            width: MediaQuery.of(context).size.width / 2,
            child: Padding(
              padding: const EdgeInsets.all(5),
              child: journalEntryDetails
            )
          )
        ]
      ),
      floatingActionButton: addJournalEntryButton(),
    );
  }

  PreferredSizeWidget journalEntriesAppBar() {
    return AppBar(
      leading: Container(),
      title: const Center(
        child: Text('Journal Entries')
      )
    );
  }

  Widget journalEntriesEnddrawer() {
    return DarkModeEnddrawer(
      changeTheme: widget.changeTheme,
      preferences: widget.preferences
    );
  }

  void updateJourneyEntryDetails(JournalEntry entry) {
    setState( () {
      journalEntryDetails = JournalEntryDetails(journalEntry: entry);
    });
  }

  Widget addJournalEntryButton() {
    return FloatingActionButton(
      child: const Icon(Icons.add),
      onPressed: () {
        Navigator.of(context).pushNamed('new_je', arguments: loadJournalEntries);
      }
    );
  }
}