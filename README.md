twitter.me
==========

The mini-twitter project for Everything.Me, by Amit Davidi.

The project has been written in Python 2.7. It runs a Mongo-DB to store data, with a single collection - 'users' for storing users' data.


API
---

The project provides the following web-API calls:
* `/user/create?uname=[User Name]` - Create a new system user; The ID (an integer) will be automatically set by the system and it's value will be encoded into the response. 
   * *uname* is mandatory
* `/user/follow?uid=[User ID]&fuid=[Follow-user ID]` - Set up user *uid* to start following user *fuid*.
* `/user/unfollow?uid=[User ID]&ufuid=[Unfollow-user ID]` - Set up user *uid* to stop following user *ufuid*.
* `/user/tweet?uid=[User ID]&m=[Message]` - Tweet a message, as specified in *m*.
* `/user/tweets/get?uid=[User ID]` - Get a user's (global) feed of tweets, i.e. the accumulation of recent posts from the users they follow.
* `/tweets/get?uid=[User ID]&fuid=[Followed-user ID]` - Retrieve the feed of the user specified by *fuid*.
 
Notes:

1. Note the *uid* parameter is a mandatory parameter in all calls and is essentially used as an alternate means of user-identification in this session-less system.
2. All responses are in JSON format and will contain the following set of fields, which differ in case of success or failure:
  * Upon success:
    * "success" : "true"
    * "payload" : [Actual data]
  * Upon an error:
    * "success" : "false"
    * "error" : [A text string describing the error]



Software overview
-----------------

The code is physically and conceptually splitted into distinct tiers, semantically organized one on top of the other to form this concept:
each tier uses the one below, but not the other way around.

This split allows for the decoupling and encapsulation of some of the core aspects of the application, described by the list below (organized according to the dependency scheme):


1. Web tier: The actual server, handling HTTP requests using designated controllers.
2. Application tier (*domain*): The application's main business logic.
3. Data / Persistence tier (*model*): The data read/write and organization layer, interfacing the DB.

As a bottom line, the project is organized such that the web tier is always the 1st one invoked (upon HTTP requests), and it uses the app tier, which in turn uses the data tier.

