Android Apps
by Joshua Luo

Developed with Google's Flutter SDK in the Dart language.


Call Me Maybe
- An application with a business card, resume, and magic eight ball predictor for call backs.
- Features a three-tab navigation that is responsive to different orientations
- The business card tab invokes platform services such as opening a text messaging app when tapping a phone number and opening a web page when tapping a web site url. Also reorganizes itself for landscape orientations.
- The resume tab displays a scrolling list of (made-up) work history elements. Purposefully does not use a ListView Widget.
- The predictor tab features a "magic eight ball" model that changes the state of the screen when tapped.

Journal
- An application for modeling a journal where the user can create journal entries with a date, title, body, and rating.
- In a portrait orientation, the entry list screen displays entry details on the right half.
- Utilizes local sqlite database to store, retrieve, and update joural entries to persists between application restarts.
- Features a app-wide dark mode option that persists between application restarts via Shared Preferences
- Features form verification for creating new journal entries.
- Makes asynchronous calls for accessing the journal entry database.
- Navigates via routes using a stack.

Wasteagram
- An application for documenting daily food waste (e.g. for a restaurant) in the form of posts.
- Features Google's Cloud Storage and Firebase Cloud Firestore for storing images and post data (number of food waste).
- Automatically retrieves the user's location (longitude, latitude) when creating a new post.
- Utilizes camera hardware to take a photo when creating a new post.
- Includes simple unit tests for a model class of a Waste Post.