import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'package:location/location.dart';
import 'package:flutter/services.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_storage/firebase_storage.dart';
import 'package:path/path.dart' as Path;
import '../widgets/post_image.dart';


class NewPostScreen extends StatefulWidget {
  const NewPostScreen({ Key? key }) : super(key: key);

  @override
  State<NewPostScreen> createState() => NewPostScreenState();
}

class NewPostScreenState extends State<NewPostScreen> {

  final formKey = GlobalKey<FormState>();
  int? quantity;
  File? image;
  final picker = ImagePicker();
  late LocationData? locationData;
  var locationService = Location();

  @override
  void initState() {
    super.initState();
    getImage();
    retrieveLocation();
  }

  void getImage() async {
    final pickedFile = await picker.pickImage(source: ImageSource.camera);
    image = File(pickedFile!.path);
    setState( () {});
  }

  void retrieveLocation() async {
    try {
      var _serviceEnabled = await locationService.serviceEnabled();
      if (!_serviceEnabled) {
        _serviceEnabled = await locationService.requestService();
        if (!_serviceEnabled) {
          print('Failed to enable service. Returning.');
          return;
        }
      }

      var _permissionGranted = await locationService.hasPermission();
      if (_permissionGranted == PermissionStatus.denied) {
        _permissionGranted = await locationService.requestPermission();
        if (_permissionGranted != PermissionStatus.granted) {
          print('Location service permission not granted. Returning.');
        }
      }

      locationData = await locationService.getLocation();
    } on PlatformException catch (e) {
      print('Error: ${e.toString()}, code: ${e.code}');
      locationData = null;
    }
    locationData = await locationService.getLocation();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: appBar(),
      body: image == null ?
        const Center(child: CircularProgressIndicator())
        : PostImage(
          image: image as File,
          formKey: formKey,
          updateQuantityFunc: updateQuantity
        ),
      floatingActionButton: uploadButton(context),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked
    );
  }
  
  PreferredSizeWidget appBar() {
    return AppBar(
      leading: Semantics(
        child: const BackButton(),
        button: true,
        enabled: true,
        onTapHint: 'Go back to view all posts.'
      ),
      title: Semantics(
        child: const Text('New Post'),
        onTapHint: 'Currently creating a new wast post.'
      ),
      centerTitle: true
    );
  }

  void updateQuantity(String value) {
    quantity = int.tryParse(value);
  }

  Widget uploadButton(BuildContext context) {
    return FractionallySizedBox(
      heightFactor: 0.1,
      widthFactor: 1,
      child: FloatingActionButton(
        child: const Icon(Icons.cloud_upload),
        onPressed: () {
          if (image == null) {
            Navigator.of(context).pushNamed('/');
          }
          if (formKey.currentState!.validate()) {
            formKey.currentState!.save();
            uploadData();
            Navigator.of(context).pushNamed('/');
          }
        },
        shape: const BeveledRectangleBorder(
          borderRadius: BorderRadius.zero
        ),
      )
    );
  }

  Future uploadData() async {
    // upload image to Firebase Storage
    String imagePath = Path.basename(image!.path);
    Reference ref = FirebaseStorage.instance.ref().child(imagePath);
    await ref.putFile(image as File);

    // get image URL
    String imageURL = await ref.getDownloadURL();

    FirebaseFirestore.instance.collection('waste_posts').add({
      'date': DateTime.now(),
      'imageURL': imageURL,
      'quantity': quantity,
      'latitude': locationData!.latitude,
      'longitude': locationData!.longitude
    });
  }
}