import 'package:flutter/material.dart';
import 'package:url_launcher/url_launcher.dart';

class BusinessCardScreen extends StatelessWidget {

  const BusinessCardScreen({ Key? key }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    if (MediaQuery.of(context).orientation == Orientation.portrait) {
      return buildPortrait(context);
    } else {
      return buildLandscape(context);
    }
  }

  Widget buildPortrait(BuildContext context) {
    return Column(
      mainAxisAlignment: MainAxisAlignment.start,
      children: [
        SizedBox(
          height: relativeHeight(context, 0.1)
          ),
        SizedBox(
          width: relativeHeight(context, 0.2),
          height: relativeHeight(context, 0.2),
          child: Padding(
            padding: EdgeInsets.all(relativeWidth(context, 0.01)),
            child: Image.asset('assets/images/joshua.png')
          )
        ),
        Padding(
          padding: EdgeInsets.all(relativeWidth(context, 0.05)),
          child: const Text(
            'Joshua Luo',
            style: TextStyle(
              fontFamily: 'Yellowtail',
              color: Colors.green,
              fontSize: 30)
          )
        ),
        Padding(
          padding: EdgeInsets.all(relativeWidth(context, 0.01)),
          child: const Text(
            'Software Engineer',
            style: TextStyle(
              decoration: TextDecoration.underline)
          )
        ),
        Padding(
          padding: EdgeInsets.all(relativeWidth(context, 0.01)),
          child: GestureDetector(
            onTap: () => launch('sms:5555555555'),
            child: Text('555-555-5555', style: Theme.of(context).textTheme.subtitle2)
          )
        ),
        Padding(
          padding: EdgeInsets.all(relativeWidth(context, 0.01)),
          child: GestureDetector(
            onTap: () => launch('https://github.com/joshluo123'),
            child: const Text('https://github.com/joshluo123', style: TextStyle(color: Colors.blue))
          )
        ),
        Padding(
          padding: EdgeInsets.all(relativeWidth(context, 0.01)),
          child: Text('luojo@oregonstate.edu', style: Theme.of(context).textTheme.subtitle2)
        )
      ]
    );
  }

  Widget buildLandscape(BuildContext context) {
    return Row (
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        SizedBox(
        width: relativeWidth(context, 0.3),
        height: relativeWidth(context, 0.3),
        child: Padding(
          padding: EdgeInsets.all(relativeHeight(context, 0.01)),
          child: Image.asset('assets/images/joshua.png')
          )
        ),
      
        Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            Padding(
              padding: EdgeInsets.all(relativeWidth(context, 0.01)),
              child: const Text(
                'Joshua Luo',
                style: TextStyle(
                    fontFamily: 'Yellowtail',
                    color: Colors.green,
                    fontSize: 30)
              )
            ),
            
            Padding(
              padding: EdgeInsets.all(relativeWidth(context, 0.01)),
              child: const Text(
                'Software Engineer',
                style: TextStyle(
                  decoration: TextDecoration.underline)
              )
            ),

            Padding(
              padding: EdgeInsets.all(relativeWidth(context, 0.01)),
              child: GestureDetector(
                onTap: () => launch('sms:5555555555'),
                child: Text('555-555-5555', style: Theme.of(context).textTheme.subtitle2)
              )
            ),

            Padding(
              padding: EdgeInsets.all(relativeWidth(context, 0.01)),
              child: GestureDetector(
                onTap: () => launch('https://github.com/joshluo123'),
                child: const Text('https://github.com/joshluo123', style: TextStyle(color: Colors.blue))
              )
            ),

            Padding(
              padding: EdgeInsets.all(relativeWidth(context, 0.01)),
              child: Text('luojo@oregonstate.edu', style: Theme.of(context).textTheme.subtitle2)
            )
          ]
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