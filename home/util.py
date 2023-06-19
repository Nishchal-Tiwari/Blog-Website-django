import random, string

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def generateSlug(title):
    from home.models import blog
    if(blog.objects.filter(title=title).exists()):
        return title + ' '+ randomword(5)
    return title