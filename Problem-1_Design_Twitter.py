# APPROACH  
# Time Complexity : O(n + m), n: total number of tweets, m: total number of users
# Space Complexity : O(n + m), as m tweet object will be created and length of the user-user mapping would be n (worst case if everyone follows each other)
# Did this code successfully run on Leetcode : Yes
# Any problem you faced while coding this : heapq custom sort function (instead make sure that the first part of the tuple you are adding to the priority queue must be the key
#                                           to the sort function)
#
#
# Your code here along with comments explaining your approach
# 1. Have Tweet object that stores time at which it was created and ID
# 2. Maintain user-user mapping (followed), each time follows is called, create an entry here key: follower and value: followee (set so that no duplicate entries). Also every 
#    person follows itself.
# 3. For unfollow function, make sure the person can't unfollow himself and delete the entry in it's hashmap
# 4. Maintain a user-tweet mapping (tweet), key: userId and value: Tweet object. make sure the userId is also present in followed mapping. have a global time counter. 
# 5. To get news feed, use priority queue. For a particular user, get all it's followee IDs and insert all their tweets into the priority queue (insert as a tuple (time, ID) as 
#    objects are not allowed in heapq in Python. Once the priority queue exceeds the feed size, pop it. Then to get final news feed, pop from the queue and insert at begining of
#    the result list (only the second part of the tuple - Id), so that the most recent one is at the top.

class Tweet:
    def __init__(self, ID, timestamp):
        self.tweet_ID = ID
        self.created_at = timestamp
        
        
class Twitter:

    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.followed = {}
        self.tweet_user_map = {}
        self.feed_size = 10
        self.time = 0
        

    def postTweet(self, userId: int, tweetId: int) -> None:
        """
        Compose a new tweet.
        """
        if userId not in self.followed:
            self.followed[userId] = set()
            self.followed[userId].add(userId)
            
        if userId not in self.tweet_user_map:
            self.tweet_user_map[userId] = []
        new_tweet = Tweet(tweetId, self.time)
        self.time += 1
        self.tweet_user_map[userId].append(new_tweet)
        

    def getNewsFeed(self, userId: int) -> List[int]:
        """
        Retrieve the 10 most recent tweet ids in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user herself. Tweets must be ordered from most recent to least recent.
        """
        priority_queue = []
        if userId not in self.followed:
            self.followed[userId] = set()
            self.followed[userId].add(userId)
            
        followee_ID = self.followed[userId]
        for each_ID in followee_ID:
            if each_ID in self.tweet_user_map:
                for ind in range(len(self.tweet_user_map[each_ID])):
                    heapq.heappush(priority_queue, (self.tweet_user_map[each_ID][ind].created_at, self.tweet_user_map[each_ID][ind].tweet_ID))

                    if len(priority_queue) > self.feed_size:
                        heapq.heappop(priority_queue)
           
        news_feed = []
        while len(priority_queue) > 0:
            news_feed.insert(0, heapq.heappop(priority_queue)[1])
            
        return news_feed
        

    def follow(self, followerId: int, followeeId: int) -> None:
        """
        Follower follows a followee. If the operation is invalid, it should be a no-op.
        """
        if followerId not in self.followed:
            self.followed[followerId] = set()
            self.followed[followerId].add(followerId)
        self.followed[followerId].add(followeeId)
        

    def unfollow(self, followerId: int, followeeId: int) -> None:
        """
        Follower unfollows a followee. If the operation is invalid, it should be a no-op.
        """
        if followerId != followeeId and followerId in self.followed and followeeId in self.followed[followerId]:
            self.followed[followerId].remove(followeeId)


# Your Twitter object will be instantiated and called as such:
# obj = Twitter()
# obj.postTweet(userId,tweetId)
# param_2 = obj.getNewsFeed(userId)
# obj.follow(followerId,followeeId)
# obj.unfollow(followerId,followeeId)
