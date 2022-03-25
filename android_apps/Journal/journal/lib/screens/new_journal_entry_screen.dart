import 'package:intl/intl.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../darkmode_enddrawer.dart';
import '../db/database_manager.dart';
import '../db/journal_entry_dto.dart';


class NewJournalEntryScreen extends StatefulWidget {

  final void Function(bool) changeTheme;
  final SharedPreferences preferences;

  const NewJournalEntryScreen({ Key? key, required this.changeTheme, required this.preferences }) : super(key: key);

  @override
  NewJournalEntryScreenState createState() => NewJournalEntryScreenState();
}


class NewJournalEntryScreenState extends State<NewJournalEntryScreen> {
  
  final formKey = GlobalKey<FormState>();
  final journalEntryFields = JournalEntryDTO();
  String dropdownValue = '-';
  static final dropDownItems = ['-', '1', '2', '3', '4'].map<DropdownMenuItem<String>>(
    (String value) {
      return DropdownMenuItem<String>(
        value: value,
        child: Text(value)
      );
    }).toList();
  
  @override
  Widget build(BuildContext context) {

    final Function() receivedFunc = ModalRoute.of(context)?.settings.arguments as Function();

    return Scaffold(
      appBar: AppBar(
        leading: const BackButton(),
        title: const Center(
          child: Text('New Journal Entry')
        ),
      ),
      endDrawer: DarkModeEnddrawer(
        changeTheme: widget.changeTheme,
        preferences: widget.preferences
      ),
      body: SingleChildScrollView(
        child: Form(
          key: formKey,
          child: Column(
            children: [
              titleForm(),
              bodyForm(),
              ratingForm(),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  saveButton(rebuildFunc: receivedFunc),
                  cancelButton()
                ]
              )
            ]
          )
        )
      ) 
    );
  }

  Widget titleForm() {
    return Padding(
      padding: const EdgeInsets.all(5),
      child: TextFormField(
        decoration: const InputDecoration(
          labelText: 'Title',
          border: OutlineInputBorder()
        ),
        onSaved: (value) {
          journalEntryFields.title = value!;
        },
        validator: (value) {
          if (value == '') {
            return 'Please enter a title';
          } 
          return null;
        }
      )
    );
  }

  Widget bodyForm() {
    return Padding(
      padding: const EdgeInsets.all(5),
      child: TextFormField(
        decoration: const InputDecoration(
          labelText: 'Body',
          border: OutlineInputBorder()
        ),
        onSaved: (value) {
          journalEntryFields.body = value!;
        },
        validator: (value) {
          if (value == '') {
            return 'Please enter a title';
          } 
          return null;
        }
      )
    );
  }

  Widget ratingForm() {
    return Padding(
      padding: const EdgeInsets.all(5),
      child: DropdownButtonFormField(
        decoration: const InputDecoration(
          labelText: 'Rating',
          border: OutlineInputBorder()
        ),
        value: dropdownValue,
        items: dropDownItems,
        onChanged: (String? newValue) {
          setState( () => dropdownValue = newValue!);
        },
        onSaved: (value) {
          journalEntryFields.rating = value.toString();
        },
        validator: (value) {
          if (value == '-') {
            return 'Please select a rating';
          }
          return null;
        }
      )
    );
  }

  Widget saveButton({required Function() rebuildFunc}) {
    return ElevatedButton(
      child: const Text('Save'),
      onPressed: () {
        if (formKey.currentState!.validate()) {
          formKey.currentState!.save();
          addDateToJournalEntryFields();

          final databaseManager = DatabaseManager.getInstance();
          databaseManager.saveJournalEntry(dto: journalEntryFields, rebuildFunc: rebuildFunc);
          Navigator.of(context).pop();
        }
      }
    );
  }

  Widget cancelButton() {
    return ElevatedButton(
      child: const Text('Cancel'),
      onPressed: () {
        Navigator.of(context).pop();
      }
    );
  }

  void addDateToJournalEntryFields() {
    journalEntryFields.dateTime = DateFormat.yMMMMd('en_US').format(DateTime.now());
  }
}