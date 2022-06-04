import 'package:flutter_test/flutter_test.dart';
import 'package:wasteagram/models/waste_post.dart';


void main() {
  test('Waste Post created by initializing with named values should have correct property values', () {
    const date = 'Thu, March 10, 2022';
    const imageURL = 'testurl.com';
    const quantity = 3;
    const latitude = 2.25;
    const longitude = 10.2;

    WastePost testPost = WastePost(
      date: date,
      imageURL: imageURL,
      quantity: quantity,
      latitude: latitude,
      longitude: longitude
    );

    expect(testPost.date, date);
    expect(testPost.imageURL, imageURL);
    expect(testPost.quantity, quantity);
    expect(testPost.latitude, latitude);
    expect(testPost.longitude, longitude);
  });
}