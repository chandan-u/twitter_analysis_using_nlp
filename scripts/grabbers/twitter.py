import tweepy
import time
import json
import os
import sys



data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','data', '')




# Streaming Class
class MyStreamListener(tweepy.StreamListener):
    """
      tweepy.StreamListner receives the stream of tweets and we inherit this class
      to overried the methods on_status, on_data, on_error etc to play with this data.
    """


    def __init__(self, fprefix = 'news'):

        self.counter = 0
        self.fprefix = fprefix
        self.output  = open(data_path + fprefix + '.'
                            + time.strftime('%Y%m%d-%H%M%S') + '.json', 'a')
        self.delout  = open(data_path+'delete.txt', 'a')

    def on_status(self, status):
        jsonObj=json.dumps(status)
        self.output.write(jsonObj)
        self.output.write(os.linesep)
        #self.output.write(status + "\n")
        self.counter += 1
        if self.counter >= 20000:
            self.output.close()
            self.output = open('./data/' + self.fprefix + '.'
                               + time.strftime('%Y%m%d-%H%M%S') + '.json', 'a')
            self.counter = 0

        return


    def on_data(self, data):

        if  'in_reply_to_status' in data:
            self.on_status(data)
        elif 'delete' in data:
            delete = json.loads(data)['delete']['status']
            if self.on_delete(delete['id'], delete['user_id']) is False:
                return False
        elif 'limit' in data:
            if self.on_limit(json.loads(data)['limit']['track']) is False:
                return False
        elif 'warning' in data:
            warning = json.loads(data)['warnings']
            print warning['message']
            return false
        return True

    def on_delete(self, status_id, user_id):
        self.delout.write( str(status_id) + "\n")
        return

    def on_error(self, status):
        print(status)

    def on_limit(self, track):

        sys.stderr.write(str(track) + "\n")
        return

    def on_timeout(self):
        sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
        time.sleep(60)
        return
