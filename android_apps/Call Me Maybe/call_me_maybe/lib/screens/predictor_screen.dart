import 'package:flutter/material.dart';
import '../models/magic_eight_ball.dart';

class PredictorScreen extends StatefulWidget {

  const PredictorScreen({ Key? key }) : super(key: key);

  @override
  State<PredictorScreen> createState() => _PredictorScreenState();
}

class _PredictorScreenState extends State<PredictorScreen> {

  final MagicEightBall magicEightBall = MagicEightBall();
  String answer = '';

  @override
  Widget build(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.start,
      children: [
        SizedBox(
          height: MediaQuery.of(context).orientation == Orientation.portrait ? relativeHeight(context, 0.2): relativeWidth(context, 0.05)
        ),

        Padding(
          padding: const EdgeInsets.all(15),
          child: Text('What\'s in your future?', style: Theme.of(context).textTheme.headline4)
        ),
        
        GestureDetector(
          onTap: () { setState( () {answer = magicEightBall.shake(); } ); },
          child: Text(
                  'Ask a question... tap for an answer.',
                  style: Theme.of(context).textTheme.headline6)
        ),

        SizedBox(
          height: relativeHeight(context, 0.1)
        ),
        
        Text(answer,
          textAlign: TextAlign.center,
          style: Theme.of(context).textTheme.headline4
        )
      ]
    );
  }

  double relativeWidth(BuildContext context, double value) {
    return MediaQuery.of(context).size.width * value;
  }

  double relativeHeight(BuildContext context, double value) {
    return MediaQuery.of(context).size.height * value;
  }

}