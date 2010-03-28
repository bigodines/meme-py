from meme import Meme

# --> examples - posts
print '========== Popular memes =========='
print Meme.Posts.popular()

print '========== Popular memes from Brazil =========='
print Meme.Posts.popular(locale='pt')

print '========== Sample search =========='
posts = Meme.Posts.search('meme rocks')
print posts

print '---------- Results for "meme rocks" ----------'
for post in posts:
    print 'Content: %s' % post.content
    print 'Caption: %s' % post.caption
    print '----------------------------------------------'

print '========== Get gchapiewski Meme =========='
meme = Meme.get(name='gchapiewski')
print meme
print meme.title
print meme.description 
print meme.url

print '========== Memes that guilherme_chapiewski is following =========='
print meme.following()

print '========== 50 Memes that guilherme_chapiewski is following =========='
print meme.following(count=50)

print '========== Memes following guilherme_chapiewski Meme =========='
print meme.followers()

print '========== 50 Memes following guilherme_chapiewski Meme =========='
print meme.followers(count=50)

print '========== Getting 5 followers from gc. From 5th to 10th randomly ordered ============='
print meme.followers(offset=5,count=5)
