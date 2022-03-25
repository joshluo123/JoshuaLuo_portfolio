import 'package:flutter/material.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:intl/intl.dart';
import '../models/waste_post.dart';

class FirestoreStream extends StatelessWidget {
  const FirestoreStream({ Key? key }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return StreamBuilder(
      stream: FirebaseFirestore.instance
        .collection('waste_posts')
        .orderBy('date', descending: true)
        .snapshots(),
      builder: (context, AsyncSnapshot<QuerySnapshot> snapshot) {
        if (snapshot.data != null && snapshot.data!.docs.isNotEmpty) {
          return ListView.builder(
            itemCount: snapshot.data?.docs.length,
            itemBuilder: (context, index) {
              var post = snapshot.data!.docs[index];
              WastePost wastePost = WastePost(
                date: DateFormat('EEE, MMM d, yyyy')
                  .format(post['date']
                  .toDate()),
                imageURL: post['imageURL'],
                quantity: post['quantity'],
                latitude: post['latitude'],
                longitude: post['longitude']
              );

              return Semantics(
                child: ListTile(
                  title: Text(wastePost.date),
                  trailing: Text(wastePost.quantity.toString()),
                  onTap: () {
                    Navigator.of(context).pushNamed('view_post', arguments: wastePost);
                  }
                ),
                onTapHint: 'View post on ${wastePost.date}'
              );
            },
          );
        } else {
          return const Center(child: CircularProgressIndicator());
        }
      }
    );
  }
}