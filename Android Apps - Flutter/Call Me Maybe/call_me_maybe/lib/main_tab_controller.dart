import 'package:flutter/material.dart';
import 'screens/business_card_screen.dart';
import 'screens/predictor_screen.dart';
import 'screens/resume_screen.dart';

class MainTabController extends StatelessWidget {

  MainTabController({ Key? key }) : super(key: key);

  static const tabs = [
    Tab(text: 'Business Card'),
    Tab(text: 'Resume'),
    Tab(text: 'Predictor')
  ];

  final screens = [
    const BusinessCardScreen(),
    const ResumeScreen(),
    const PredictorScreen()
  ];

  @override
  Widget build(BuildContext context) {
    return DefaultTabController(
      length: 3,
      initialIndex: 0,
      child: Scaffold(
        appBar: AppBar(
          title: const Center(
            child: Text('Call Me Maybe')
          ),
          bottom: const TabBar(tabs: tabs)
        ),
        body: TabBarView(children: screens)
      )
    );
  }
}