
# coding: utf-8

# In[1]:


import findspark
findspark.init('/spark/')


# In[2]:


from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
from pyspark.sql.functions import desc


# In[3]:


sc = SparkContext()


# In[4]:


ssc = StreamingContext(sc,10)
sqlcontext = SQLContext(sc)


# In[5]:


socket_stream = ssc.socketTextStream("127.0.0.1",8889)


# In[6]:


lines = socket_stream.window(20)


# In[7]:


from collections import namedtuple
fields = ('tag','count')
Tweet = namedtuple('Tweet',fields)


# In[8]:


lines.flatMap( lambda text: text.split(" ") ) .filter (lambda word: word.lower().startswith("#")) .map (lambda word: (word.lower(),1) ) .reduceByKey ( lambda a,b: a+b ) .map ( lambda rec: Tweet(rec[0],rec[1]) ) .foreachRDD ( lambda rdd: rdd.toDF().sort(desc('count'))
.limit(10).registerTempTable('tweets') )


# In[16]:


ssc.start()


# In[10]:


import time
from IPython import display
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[12]:


count = 0
while count < 10:
    time.sleep(3)
    top_10_tweets = sqlcontext.sql( 'Select tag,count from tweets' )
    top_10_df = top_10_tweets.toPandas()
    display.clear_output(wait=True)
    plt.figure( figsize = (10,8) )
    sns.barplot(x="count",y="tag", data=top_10_df)
    plt.show()
    count = count+1


# In[15]:


ssc.stop()

