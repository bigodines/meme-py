import yql

API_KEY = 'dj0yJmk9RW1TaFkzN1NNcVFMJmQ9WVdrOVJXRlZjbnBpTm1zbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1hYg--' # gc
SECRET = 'd09162c0f9d12b3845668301a2776bec8fa5bd23' # gc

class MemeNotFound(Exception):
    """Raised when Meme is not found."""

class Repository(object):
    def __init__(self):
        self.yql = yql.Public()
        self.yql_private = None
    
    #TODO
    # def _private_yql_query(self, query):
    #    if not self.yql_private:
    #        self.yql_private = yql.ThreeLegged(API_KEY, SECRET)
    #        request_token, auth_url = self.yql_private.get_token_and_auth_url()
    #        access_token = self.yql_private.get_access_token(request_token, verifier)
            
    #    self.yql_private.execute(query, token=access_token)

class MemeRepository(Repository):
    def _yql_query(self, query):
        result = self.yql.execute(query)
        if result.count == 1:
            return Meme(result.rows)
        return [Meme(row) for row in result.rows]
    
    def get(self, name):
        query = 'SELECT * FROM meme.info WHERE name = "%s"' % name
        meme = self._yql_query(query)
        if meme:
            return meme
        raise MemeNotFound("Meme %s was not found!" % name)
    
    def following(self, name, count=10, offset=0):
        guid = self.get(name).guid #TODO: evaluate performace impacts
        query = 'SELECT * FROM meme.following(%d,%d) WHERE owner_guid = "%s"' % (offset, count, guid)
        return self._yql_query(query)
    
    #TODO
    #def post(self, content):
    #    post_type = 'text'
    #    query = 'INSERT INTO meme.user.posts (type, content) VALUES ("%s", "%s")' % (post_type, content)
    #    self._private_yql_query(query)
        
    def followers(self, name, count=10, offset=0):
        guid = self.get(name).guid #TODO: evaluate performace impacts
        query = 'SELECT * FROM meme.followers(%d,%d) WHERE owner_guid = "%s"' % (offset, count, guid)
        return self._yql_query(query)
    
class PostRepository(Repository):
    def _yql_query(self, query):
        result = self.yql.execute(query)
        if result.count == 1:
            return [Post(result.rows)]
        return [Post(row) for row in result.rows]

    def popular(self, locale, count, offset=0):
        query = 'SELECT * FROM meme.popular(%d,%d) WHERE locale="%s"' % (offset, count, locale)
        return self._yql_query(query)
    
    def searchByUser(self, user, count=100, offset=0):
        query = 'SELECT * FROM meme.posts WHERE owner_guid in (SELECT guid FROM meme.info WHERE name = "%s") LIMIT %d, %d' % (user, offset, count)
        return self._yql_query(query)

    def search(self, query, count, offset=0):
        query = 'SELECT * FROM meme.search(%d,%d) WHERE query="%s"' % (offset, count, query)
        return self._yql_query(query)

class Meme(object):
    def __init__(self, data=None):
        if data:
            self.guid = data['guid']
            self.name = data['name']
            self.title = data['title']
            self.description = data['description']
            self.url = data['url']
            self.avatar_url = data['avatar_url']
            self.language = data['language']
            self.follower_count = data['followers']
        
        self.meme_repository = MemeRepository()
    
    def following(self, count=10, offset=0):
        return self.meme_repository.following(self.name, count, offset)
    
    def followers(self, count=10, offset=0):
        return self.meme_repository.followers(self.name, count, offset)
        
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
