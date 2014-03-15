twitter.me
==========

The mini-twitter project for Everything.Me, by Amit Davidi.

The project has been written in Python 2.7. It runs a Mongo-DB to store data, with a single collection - 'users' for storing users' data.

The project provides the following web-API calls:
* `/user/create?uname=[User Name]` - Create a user in the system; The ID will be automatically set by the system and encoded into the response. 
   * *uname* is mandatory
* `/user/follow?uid=[User ID]&fuid=[Follow-user ID]` - Set up user *uid* to start following user *fuid*.
* `/user/unfollow?uid=[User ID]&ufuid=[Unfollow-user ID]` - Set up user *uid* to stop following user *ufuid*.
* `/user/tweet?uid=[User ID]&m=[Message]` - Tweet a message, as specified in *m*.
* `/user/tweets/get?uid=[User ID]` - Get a user's (global) feed of tweets, i.e. the accumulation of recent posts from the users they follow.
* `/tweets/get?uid=[User ID]&fuid=[Followed-user ID]` - Retrieve the feed of the user specified by *fuid*.
 
 Notes:
1. In all calls, note the *uid* parameter is mandatory and is essentially used as an alternate means of identification in this session-less system.
2. all responses are in JSON format and will contain the following set of fields, which differ in case of success or failure:
  * Upon success:
    * "success" : "true"
    * "payload" : [Actual data]
  * Upon error:
    * "success" : "false"
    * "error" : [A text string describing the error]



Software overview
=================

The code that makes up this project is splitted into tiers organized one on top of the other: each tier uses the one below, but no the other way around.
This split allows for the decoupling and encapsulation of some of the core aspects of the application.
The following list describes are the layers, ordered according to dependency:
1. Web tier: The actual server, handling HTTP requests using designated controllers.
2. Application tier (*domain*): The application's main business logic.
3. Data / persistence tier (*model*): The data read/write and organization layer, interfacing the DB.
