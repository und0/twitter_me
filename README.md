twitter.me
==========

The mini-twitter project for Everything.Me, by Amit Davidi.

The project provides the following web-API calls:
 * `/user/create?uname=[User Name]` - Create a user in the system; The ID will be automatically set by the system and encoded into the response. 
   * *uname* is mandatory
 * `/user/follow?uid=[User ID]&fuid=[Follow-user ID]` - Sign up user *uid* to start follow user *fuid*.
 * `/user/unfollow?uid=[User ID]&ufuid=[Unfollow-user ID]` - Unfollow a user.
 * `/user/tweet?uid=[User ID]&m=[Message]` - Tweet a message, as specified in *m*.
 * `/user/tweets/get?uid=[User ID]` - Get a user's (global) feed of tweets, i.e. the accumulation of recent posts from the users they follow.
 * `/tweets/get?uid=[User ID]&fuid=[Followed-user ID]` - Retrieve the feed of the user specified by `fuid`.
 
 Do note that for all calls, note the *uid* parameter is mandatory and is essentially used as an alternate means of identification in this session-less system.
 In addition, all responses are in JSON format and will contain the following set of fields, which differ in case of success or failure:
 * Upon success:
   * "success" : "true"
   * "payload" : "Actual data"
 * Upon error:
   * "success" : "false"
   * "error" : "An error message"
