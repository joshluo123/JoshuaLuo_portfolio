import 'dart:io';
import 'package:flutter/material.dart';
import 'quantity_form.dart';

class PostImage extends StatelessWidget {

  final File image;
  final GlobalKey<FormState> formKey;
  final Function(String) updateQuantityFunc;

  const PostImage({
    Key? key,
    required this.image,
    required this.formKey,
    required this.updateQuantityFunc})
    : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      child: SingleChildScrollView(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Semantics(
              child: Padding(
                padding: const EdgeInsets.all(10),
                child: SizedBox(
                  width: MediaQuery.of(context).size.width,
                  height: MediaQuery.of(context).size.height * 0.5,
                  child: Image.file(image)
                )
              ),
              onTapHint: 'Image for this new post',
            ),
            Semantics(
              child: Padding(
                padding: const EdgeInsets.all(10),
                child: Center(
                  child: QuantityForm(formKey: formKey, updateQuantityFunc: updateQuantityFunc)
                )
              ),
              onTapHint: 'Enter a number of wasted items.'
            )
          ]
        )
      ),
      button: true,
        enabled: true,
        onTapHint: 'Upload post to Wasteagram'  
    );
  }
}