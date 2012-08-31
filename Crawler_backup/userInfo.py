##userinfo is a class to hold all the user information for the mysql database
# if anything needs to change it can be changed in here.

class userInfo:
    def __init__(self):
        self.username = 'crawler';
        self.password = 'crawlerpass';
        self.database = 'uummuu_';
        self.server = '127.0.0.1';
