import 'package:flutter/material.dart';
import '../models/waste_post.dart';

class DetailScreen extends StatelessWidget {

  const DetailScreen({ Key? key }) : super(key: key);

  @override
  Widget build(BuildContext context) {

    final WastePost receivedPost = ModalRoute.of(context)?.settings.arguments as WastePost;

    return Scaffold(
      appBar: appBar(receivedPost.date),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        children: [
          postDate(receivedPost.date),
          postImage(context, receivedPost.imageURL),
          postQuantity(receivedPost.quantity),
          postLocation(receivedPost.latitude, receivedPost.longitude)
        ]
      ),
    );
  }

  PreferredSizeWidget appBar(date) {
    return AppBar(
      leading: Semantics(
        child: const BackButton(),
        button: true,
        enabled: true,
        onTapHint: 'Go back to view all posts'),
      title: Semantics(
        child: const Text('Wasteagram'),
        onTapHint: 'Currently viewing a post on $date'
      ),
      centerTitle: true,
    );
  }

  Widget postDate(date) {
    return Semantics(
      child: Padding(
        padding: const EdgeInsets.only(top: 40, bottom: 30),
        child: Text(
          date,
          style: const TextStyle(
            fontSize: 24)
        )
      ),
      onTapHint: 'This post was made on $date'
    );
  }

  Widget postImage(BuildContext context, imageURL) {
    return Semantics(
      child: Center(
        child: SizedBox(
          width: MediaQuery.of(context).size.width * 0.9,
          height: MediaQuery.of(context).size.height * 0.5,
          child: Image.network(imageURL)
        )
      ),
      onTapHint: 'Picture for this post',
    );
  }

  Widget postQuantity(quantity) {
    return Semantics(  
      child: Padding(
        padding: const EdgeInsets.only(top: 20, bottom: 20),
        child: Text(
          '$quantity items',
          style: const TextStyle(
            fontSize: 36
          )
        )
      ),
      onTapHint: 'This post has $quantity waste items.'
    );
  }

  Widget postLocation(latitude, longitude) {
    return Semantics(
      child: Padding(
        padding: const EdgeInsets.only(top: 50),
        child: Text(
          'Location: $latitude, $longitude'
        )
      ),
      onTapHint: 'Location of this post'
    );
  }
}