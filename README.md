twitter.me
==========

The mini-twitter project for Everything.Me, by Amit Davidi.

The project has been written in Python 2.7.

Data is stored using the MongoDB technology.


API
---

The project provides the following web-API calls:
* `/user/create?uname=[User Name]` - Create a new system user; The ID (an integer) will be automatically set by the system and it's value will be encoded into the response. *uname* is mandatory
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

As a bottom line, the project is organized such that the web tier is always the 1st one invoked (upon HTTP requests), and, in order to complete
the handling of thsoe requests, 'uses' the app tier, which in turn 'uses' the data tier.

The following sections provide an overview of the tiers, bottom to top.


### Data Tier

The lowest tier. Handles and manages data storage.

As far as data design is concerned, only a single Mongo collection called 'users' holds user-data documents; associated posts (tweets) are stored as a list property of embedded documents over the user document.
Seeing that order matters a great deal in posts (users usually care more for new posts rather than old ones), each post holds its creation date, and thus the list is at all times sorted according to that date.


Physically speaking, the tier is organized in 3 packages:

1. db - Pure DB concerns.
2. humongolus - A 3rd party ORM package; actually only very minimally used, as it has been found buggy and incomplete, due to these two major issues:
  * Embedded documents (such as posts in our case) are not read in 'find' queries.
  * It's API is not generic enough to allow for complex queries.
3. model - Entities and DAO's:
  * UserEntity - The object representation of the user documents.
  * UserPost <-- PostMessage - A user's message post; inheritance in this case allows for posting polymorphism (textual posts, audio, video posts, etc).


### Application Tier

The middle tier. Organized as just a single module in a single package: UserManagement under *domain*.

Provides a neat OOD abstraction of the business logic layer (involving user management).


### Web Tier

The upper tier. Organized as several modules under a package called 'web'.

It's main component is a simplified front-controller, which invokes request handling controllers; this is used as a simplified substitute for the 'VC' parts of traditional MVC frameworks.


### Additional code

* AppContext - application context allowing for primitive Dependency Injection concepts.
* twitter_me.py - 'main' module.
