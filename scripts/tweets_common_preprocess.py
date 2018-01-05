"""

  __author__ = { name: "Chandan Uppuluri",
                 email_id:"chandan.uppuluri@gmail.com" }

  does common preprocessing to tweets:
    remove URL's
    remove pucntuations (NOT hash tags '#')
    remove emoji's
    remove smiley's
    remove mentions's
    remove retweets (duplicates only) (store original tweet)
    remove RESERVE words: RT etc

    retain hashtags
    retain numbers
  different analysis requires different preprocessing.
  Modify this script based on the requirements


  TODO: Need to create multiple output files instead of one data.csv file in ./data/clean
  This way we can use spark in distributed fashion and work on multiple files in parallel.
  Most of the tasks done in this project: word2vec, wordcount, hashtag, preprocessing, pos tagging
  etc., can be implemented using spark.


"""
# to deal with encoding issues (non ascii characters)
import sys
reload(sys)
sys.setdefaultencoding('utf8')


import os
import json
import csv
from pprint import pprint
import time

# tweet preprocessing lib/config
import preprocessor as p

# p.OPT.NUMBER, p.OPT.HASHTAG
# (do process them induvidually in analysis phase if required)
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.SMILEY, p.OPT.MENTION, p.OPT.RESERVED)


# regex to remove punctuations.
import re
import string

# '#' not included to save the space.
punctuations = '!"$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
regex = re.compile('[%s]' % re.escape(punctuations))
regexb=re.compile('b[\'\"]')

# data : read and write directory paths
read_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data', 'raw', '')
write_data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data', 'clean', '')

def preprocessTweets(filepath):

    """
        read the json data from the given filepath
        return a list of the json objects

        preprocess rules:

            remove URL's
            remove pucntuations (NOT hash tags '#')
            remove emoji's
            remove smiley's
            remove mentions's
            remove retweets (duplicates only) (store original tweet)
            remove RESERVE words: RT etc

        NOTE: this function can be modifed as we please because its the main nerve center for the entire program
    """

    # write processed tweets to a csv
    out_file_path = os.path.join( write_data_path, 'data.csv') #outfile path
    out_file = open( out_file_path, "a")  # out_file obj
    csv_writer  = csv.writer(out_file, delimiter=',', lineterminator='\r\n', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(["id", "text", "date"])  #write header

    # process each tweet (memory efficient for large files)
    id_list = []
    with open(filepath, 'r') as fileobj:
        for line in fileobj:

            try:
                # raw data is doubly encoded json, pass it twice through json.loads
                line =  json.loads(line)
                obj =  json.loads(line)
                #pprint(obj)



                # handle retweets/duplicates: save original tweet if retweet (and remove duplicates)
                if "retweet_status" in obj.keys():
                    retweet_id = obj["retweet_status"]["id_str"]
                    if retweet_id in id_list:
                        continue

                    retweet_message = obj["retweet_status"]["u'extended_tweet"]["u'full_text"]
                    created_at = obj["retweet_status"]["created_at"]
                    tweet = retweet_message.encode('utf-8').strip()
                    message_id = retweet_id
                    created_at = time.strftime('%Y-%m-%d %H', time.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y'))

                else:
                    tweet=obj['text'].encode('utf-8').strip()
                    message_id=obj['id_str']
                    created_at = time.strftime('%Y-%m-%d %H', time.strptime(obj["created_at"], '%a %b %d %H:%M:%S +0000 %Y'))

                # remove url, emoji's, smirley's, mentions (you can choose to retain mentions)
                # refer Global variable p.set_options
                tweet = p.clean(tweet)         # remove urls, reserved, emoji, smiley, mention
                tweet = tweet.lower()          # lower
                tweet = regexb.sub('', tweet)  # remove punctuations
                tweet = regex.sub('', tweet)   # remove quotes
                print tweet, message_id, type(tweet), type(message_id)
                csv_writer.writerow([message_id, tweet, created_at])

            except:
                continue

    # close outfile
    out_file.close()


# returns the absolute paths of files presnet in a directory
# ("json files only")
def getFilePaths(directory):
    """
       returns a list of full paths for all the json files
       present in the given directory
    """

    list_of_filepaths=[]
    for root, dirs, filenames in os.walk(directory):
        for f in filenames:
            if f.endswith('.json') :
                list_of_filepaths.append( os.path.join(root, f))
    return list_of_filepaths

files = getFilePaths(read_data_path)

# preprocess all the raw json files
# output to data/clean/data.csv file
for filepath in files:
    preprocessTweets(filepath)
