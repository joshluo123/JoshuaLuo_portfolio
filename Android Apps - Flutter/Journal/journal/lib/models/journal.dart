import 'package:flutter/material.dart';
import 'journal_entry.dart';

class Journal extends StatelessWidget {

  final List<JournalEntry> entries;
  final Function(JournalEntry) updateJourneyEntryDetails;

  const Journal({ Key? key, required this.entries, required this.updateJourneyEntryDetails }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (entries.isEmpty) {
      return welcome(context);
    } else {
      return journalEntryList(context);
    }
  }

  Widget welcome(BuildContext context) {
    return Column(
      children: [
        SizedBox(
          width: 0,
          height: MediaQuery.of(context).size.height * 0.1
        ),
        const Center(
          child: Text(
            'Welcome to your journal!',
            style: TextStyle(
              fontSize: 30
            )
          )
        ),
        SizedBox(
          width: 0,
          height: MediaQuery.of(context).size.height * 0.05
        ),
        const Center(
          child: Text(
            'Let\'s get started by adding a journal entry',
            style: TextStyle(
              fontSize: 20
            )
          )
        )
      ]
    );
  }

  Widget journalEntryList(BuildContext context) {
    return ListView.builder(
      itemCount: entries.length,
      itemBuilder: (context, index) {
        return ListTile(
          leading: const FlutterLogo(),
          title: Text(entries[index].title),
          subtitle: Text(entries[index].dateTime),
          onTap: () {
            if (MediaQuery.of(context).size.width < 700) {
              Navigator.of(context).pushNamed('view_je', arguments: entries[index]);
            } else {
              updateJourneyEntryDetails(entries[index]);
            }
          }
        );
      }
    );
  }
}