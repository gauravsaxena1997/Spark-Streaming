
# coding: utf-8

# In[ ]:


import tweepy
from tweepy import OAuthHandler,Stream
from tweepy.streaming import StreamListener
import socket,json


# In[ ]:


consumer_key = 'hqzcXRnqj5AoYr4MvTF9dbeYU' 
consumer_secret = 'jlTXxVjt3Nc0tA9fDtkwpIwoFXjXzeF4AQtGEDgni8nCy2mNES' 
access_token = '973076672231587840-Dh6SZrWFo0HcSAC82nNdXieL8ZKwF3R'
access_secret = 'pVaaWWUYZPrmOatlgAmnQTb26o1WXaQKHBJsOTZzZ94ax'


# In[ ]:


class TweetListener (StreamListener):
    def __init__(self,csocket):
        self.client_socket = csocket
        
    def on_data(self,data):
        try:
            msg = json.loads(data)
            print(msg['text'].encode('utf-8'))
            self.client_socket.send(msg['text'].encode('utf-8'))
            return True
        except BaseException as e:
            print ('Error:- ',e)
        return True
    
    def on_error(self,status):
        print(status)
        return True


# In[ ]:


def send_data(c_socket):
    auth = OAuthHandler (consumer_key,consumer_secret)
    auth.set_access_token (access_token,access_secret)
    
    twitter_stream = Stream(auth,TweetListener(c_socket))
    twitter_stream.filter(track=['#'])


# In[ ]:


if __name__== "__main__":
    s=socket.socket()
    host = '127.0.0.1'
    port = 8889
    s.bind ((host,port))
    
    print ("Listening to port...")
    s.listen(5)
    c,addr = s.accept()
    
    send_data (c)

