import 'package:flutter/material.dart';

class ResumeScreen extends StatelessWidget {

  const ResumeScreen({ Key? key }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: EdgeInsets.all(relativeWidth(context, 0.01)),
            child: const Text(
              'Joshua Luo',
              style: TextStyle(
                  fontFamily: 'Yellowtail',
                  color: Colors.green,
                  fontSize: 36))
          ),

          Padding(
            padding: EdgeInsets.all(relativeWidth(context, 0.01)),
            child: Text('555-555-5555', style: Theme.of(context).textTheme.subtitle1)
          ),

          Padding(
            padding: EdgeInsets.all(relativeWidth(context, 0.01)),
            child: Text('luojo@oregonstate.edu', style: Theme.of(context).textTheme.subtitle1)
          ),
          
          workExperience(context,
            title: 'Post-Baccalaureate Student',
            company: 'OSU',
            dates: '2020-2022',
            location: 'Corvallis, OR',
            description: 'Attented Oregon State University\'s online post-baccalaureate program in computer science.'
          ),

          workExperience(context,
            title: 'Patent Examiner',
            company: 'USPTO',
            dates: '2016-2019',
            location: 'Alexandria, VA',
            description: 'Examiend patent applications to determine the patentability of proposed inventions and innovations.'
          ),

          workExperience(context,
            title: 'Front-End Helper',
            company: 'Costco',
            dates: '2015-2016',
            location: 'Lynnwood, WA',
            description: 'Assisted front-end team with various jobs involving interaction with customers.'
          ),

          workExperience(context,
            title: 'Front-End Helper',
            company: 'Safeway',
            dates: '2015',
            location: 'Seattle, WA',
            description: 'Stocked shelves and assisted customers with shopping for groceries.'
          ),

          workExperience(context,
            title: 'Substitute Tutor',
            company: 'Bellevue Learning Center',
            dates: '2014',
            location: 'Bellevue, WA',
            description: 'Tutored middle school students in the summer in Language Arts and Math.'
          ),

          workExperience(context,
            title: 'Undergraduate Studnet',
            company: 'UW',
            dates: '2011-2015',
            location: 'Seattle, WA',
            description: 'Earned an Bachelor of Science in Electrical Engineering at the University of Washington.'
          ),

          workExperience(context,
            title: 'Tennis Instructor',
            company: 'CBRC',
            dates: '2011',
            location: 'Richland, WA',
            description: 'Taught beginner tennis to children in a group setting.'
          )
        ]
      )
    );
  }

  double relativeWidth(BuildContext context, double value) {
    return MediaQuery.of(context).size.width * value;
  }

  double relativeHeight(BuildContext context, double value) {
    return MediaQuery.of(context).size.height * value;
  }

  Widget workExperience(BuildContext context, {required title, required company, required dates, required location, required description}) {
    return Padding(
        padding: EdgeInsets.all(relativeWidth(context, 0.02)),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Padding(
              padding: EdgeInsets.all(relativeWidth(context, 0.01)),
              child: Text(
                title,
                style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 20
              ))
            ),
            Padding(
              padding: EdgeInsets.all(relativeWidth(context, 0.01)),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Text(company, style: const TextStyle(fontStyle: FontStyle.italic)),
                  Text(dates, style: const TextStyle(fontStyle: FontStyle.italic)),
                  Text(location, style: const TextStyle(fontStyle: FontStyle.italic))
                ]
              )
            ),
            Text(description, style: Theme.of(context).textTheme.bodyText2)
          ]
        )
    );
  }
}