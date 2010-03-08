import httplib
import yql

API_KEY = 'dj0yJmk9RW1TaFkzN1NNcVFMJmQ9WVdrOVJXRlZjbnBpTm1zbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1hYg--'
SECRET = 'd09162c0f9d12b3845668301a2776bec8fa5bd23'

class Repository(object):
    def __init__(self):
        self.yql = yql.Public()
        self.yql_private = None
    
    #TODO
    #def _private_yql_query(self, query):
    #    if not self.yql_private:
    #        self.yql_private = yql.ThreeLegged(API_KEY, SECRET)
    #        request_token, auth_url = self.yql_private.get_token_and_auth_url()
    #        #TODO: USER AUTHENTICATES HERE
    #        access_token = self.yql_private.get_access_token(request_token, verifier)
    #        
    #    self.yql_private.execute(query, token=access_token)

class MemeRepository(Repository):
    def __init__(self):
        super(MemeRepository, self).__init__()
    
    def _yql_query(self, query):
        result = self.yql.execute(query)
        if result.count == 1:
            return Meme(result.rows)
        
        memes = []
        for row in result.rows:
            memes.append(Meme(row))
        return memes
    
    def get(self, name):
        query = 'SELECT * FROM meme.info WHERE name = "%s"' % name
        return self._yql_query(query)
    
    def following(self, name, count):
        guid = self.get(name).guid #TODO: evaluate performace impacts
        query = 'SELECT * FROM meme.following(%d) WHERE owner_guid = "%s"' % (count, guid)
        return self._yql_query(query)
    
    #TODO
    #def post(self, content):
    #    post_type = 'text'
    #    query = 'INSERT INTO meme.user.posts (type, content) VALUES ("%s", "%s")' % (post_type, content)
    #    self._private_yql_query(query)
        
class PostRepository(Repository):
    def __init__(self):
        super(PostRepository, self).__init__()

    def _yql_query(self, query):
        result = self.yql.execute(query)
        posts = []
        for row in result.rows:
            posts.append(Post(row))
        return posts

    def popular(self, locale):
        query = 'SELECT * FROM meme.popular WHERE locale="%s"' % locale
        return self._yql_query(query)
    
    def search(self, query):
        query = 'SELECT * FROM meme.search WHERE query="%s"' % query
        return self._yql_query(query)

class Meme(object):
    def __init__(self, data):
        self.guid = data['guid']
        self.name = data['name']
        self.title = data['title']
        self.description = data['description']
        self.url = data['url']
        self.avatar_url = data['avatar_url']
        self.language = data['language']
        self.follower_count = data['followers']
        
        self.meme_repository = MemeRepository()
    
    def following(self, count=10):
        return self.meme_repository.following(self.name, count)
        
    def __repr__(self):
        return u'Meme[guid=%s, name=%s]' % (self.guid, self.name)

class Post(object):
    def __init__(self, data):
        self.guid = data['guid'] #meme id
        self.pubid = data['pubid'] #post id
        self.type = data['type']
        self.caption = data['caption']
        self.content = data['content']
        self.comment = data['comment'] if 'comment' in data else None
        self.url = data['url']
        self.timestamp = data['timestamp']
        self.repost_count = data['repost_count']
        
        #if empty then not a repost
        self.origin_guid = data['origin_guid'] if 'origin_guid' in data else None
        self.origin_pubid = data['origin_pubid'] if 'origin_pubid' in data else None
        self.via_guid = data['via_guid'] if 'via_guid' in data else None
    
    def __repr__(self):
        return u'Post[guid=%s, pubid=%s, type=%s]' % (self.guid, self.pubid, self.type)
