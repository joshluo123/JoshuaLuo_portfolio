import 'package:flutter/material.dart';
import 'package:journal/models/journal_entry.dart';


class JournalEntryDetails extends StatelessWidget {

  final JournalEntry journalEntry;

  const JournalEntryDetails({ Key? key, required this.journalEntry }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          journalEntryTitle(title: journalEntry.title),
          journalEntryBody(body: journalEntry.body),
          journalEntryRating(rating: journalEntry.rating)
        ]
      )
    );
  }

  Widget journalEntryTitle({required String title}) {
    return Padding(
      padding: const EdgeInsets.all(10),
      child: Text(
        title,
        style: const TextStyle(
          fontSize: 40,
          decoration: TextDecoration.underline
        )
      )
    );
  }

  Widget journalEntryBody({required String body}) {
    return Padding(
      padding: const EdgeInsets.all(5),
      child: Text(
        body,
        style: const TextStyle(
          fontSize: 24
        )
      )
    );
  }

  Widget journalEntryRating({required String rating}) {
    return Padding(
      padding: const EdgeInsets.all(5),
      child: Text(
        'Rating: $rating/4',
        style: const TextStyle(
          fontSize: 16
        )
        )
    );
  }
}