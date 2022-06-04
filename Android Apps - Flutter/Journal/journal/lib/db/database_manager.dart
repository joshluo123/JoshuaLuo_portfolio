// ignore_for_file: constant_identifier_names

import 'package:flutter/services.dart';
import 'package:sqflite/sqflite.dart';
import 'journal_entry_dto.dart';
import '../models/journal_entry.dart';


const String SQL_CREATE_SCHEMA_PATH = 'assets/schema_1.sql.txt';
const String SQL_INSERT_PATH = 'assets/insert.sql.txt';
const String SQL_SELECT_PATH = 'assets/select.sql.txt';

class DatabaseManager {

  static const String DATABASE_FINALNAME = 'journal.sqlite3.db';

  static DatabaseManager? _instance;
  final Database db;

  DatabaseManager._({required Database database}) : db = database;

  factory DatabaseManager.getInstance() {
    assert(_instance != null);
    return _instance as DatabaseManager;
  }

  static Future initialize() async {
    final db = await openDatabase(
      DATABASE_FINALNAME,
      version: 1,
      onCreate: (Database db, int version) async {
        createTables(db);
      }
    );
    _instance = DatabaseManager._(database: db);
  }

  static void createTables(Database db) async {
    await db.execute(await rootBundle.loadString(SQL_CREATE_SCHEMA_PATH));
  }

  void saveJournalEntry({required JournalEntryDTO dto, required Function() rebuildFunc}) async {
    db.transaction( (txn) async {
      await txn.rawInsert(
        await rootBundle.loadString(SQL_INSERT_PATH),
        [dto.title, dto.body, dto.rating, dto.dateTime]
      );
    });
    rebuildFunc();
  }

  Future<List<JournalEntry>> getJournalEntries() async {
    final List<Map> journalRecords = await db.rawQuery(await rootBundle.loadString(SQL_SELECT_PATH));
    return journalRecords.map( (record) {
      return JournalEntry(
        title: record['title'],
        body: record['body'],
        rating: record['rating'],
        dateTime: record['dateTime']
      );
    }).toList();
  }
}