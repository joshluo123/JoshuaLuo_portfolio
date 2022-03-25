import 'package:flutter/material.dart';
import '../widgets/firestore_stream.dart';


class ListScreen extends StatefulWidget {
  const ListScreen({ Key? key }) : super(key: key);

  @override
  State<ListScreen> createState() => _ListScreenState();
}

class _ListScreenState extends State<ListScreen> {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: appBar(),
      body: const FirestoreStream(),
      floatingActionButton: getPhotoButton(),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat
    );
  }

  PreferredSizeWidget appBar() {
    return AppBar(
        leading: Container(),
        title: Semantics (
          child: const Text('Wasteagram'),
          onTapHint: 'Currently viewing a list of all previous waste posts.'
        ),
        centerTitle: true,
    );
  }

  Widget getPhotoButton() {
    return Semantics(
      child: FloatingActionButton(
        child: const Icon(Icons.camera_alt),
        onPressed: () {
          Navigator.of(context).pushNamed('new_post');
        }
      ),
      button: true,
      enabled: true,
      onTapHint: 'Select an image'
    );
  }
}