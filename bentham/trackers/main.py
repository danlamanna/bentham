from events import TwitterEventTracker
from intervals import SimpleInterval

if __name__ == '__main__':
    TwitterEventTracker(SimpleInterval(60)).run()
