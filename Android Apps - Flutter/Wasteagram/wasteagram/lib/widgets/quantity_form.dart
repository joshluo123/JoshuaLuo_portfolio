import 'package:flutter/material.dart';


class QuantityForm extends StatelessWidget {

  final GlobalKey<FormState> formKey;
  final Function(String) updateQuantityFunc;

  const QuantityForm({
    Key? key,
    required this.formKey,
    required this.updateQuantityFunc})
    : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Semantics(
      child: Form(
        key: formKey,
        child: TextFormField(
          keyboardType: TextInputType.number,
          decoration: const InputDecoration(
            labelText: 'Number of Wasted items'
          ),
          onSaved: (value) {
            updateQuantityFunc(value as String);
          },
          validator: (value) {
            if (value == null || int.tryParse(value) == null) {
              return 'Please enter a number';
            }
            return null;
          }
        )
      ),
      onTapHint: 'Enter the quantity of wasted items.'
    );
  }
}