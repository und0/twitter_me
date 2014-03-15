class UserService:

    def __init__(self, user_dao):
        self.user_dao = user_dao

    def create_user(self, user_name):
        user = self.user_dao.create_user(user_name)
        return user
    
    def get_user(self, user_id):
        user = self.user_dao.get_user(user_id)
        return user

    def add_follow(self, user, follow_uid):
        self.user_dao.add_follow(user, follow_uid)
    
    def remove_follow(self, user, follow_uid):
        self.user_dao.remove_follow(user, follow_uid)
        
    def add_post(self, user, post):
        self.user_dao.add_post(user, post)
    
    def get_user_feed(self, user):
        f_users = self.user_dao.get_followed_users(user)
        
        ' Arrange users onto the form of a dictionary, with the user-id as a key '    
        user_posts = {}
        for u in f_users:
            if u.posts and len(u.posts)>0:
                user_posts[u._id] = u
        
        return user_posts
