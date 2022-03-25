import 'dart:math';

class MagicEightBall {

  final responses = [
    'It is certain.',
    'Signs point to yes.',
    'Most likely.',
    'Without a doubt.',
    'Better not tell you now.',
    'Reply hazy, try again.',
    'Don\'t count on it.',
    'My sources say no.'
  ];

  final Random random = Random();
  int currentValue = 0;

  String shake() {
    currentValue = random.nextInt(responses.length);
    return responses[currentValue];
  }
}