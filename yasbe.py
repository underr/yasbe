import toml, os, codecs, shutil
from operator import itemgetter
from mistune import markdown
from distutils import dir_util
from glob import glob
from mako.template import Template

with open("config.toml") as cc:
    config = toml.loads(cc.read()) # config dict from TOML file

posts = []
info = config["info"]

files = glob('./posts/*.md')
for fiel in files:
    content = open(fiel).read()
    ob = {} # init dict to be inserted after
    f = os.path.basename(fiel) # remove path
    date =  f.split("-")[:3]
    f_date = '-'.join(date)
    title = f.replace(f_date, "")[1:].split('.')[0]
    c_title = title[:1].upper() + title[1:].replace("-", " ")
    full = {
        "content": content,
        "file": title,
        "date": f_date,
        "title": c_title
    }   
    posts.append(full) # add post to list of posts

try:
    shutil.rmtree('./www/') # clean files on www directory
except Exception as e:
    pass
# create necessary folders and copy assets
os.mkdir("./www")
os.mkdir("./www/static")
dir_util.copy_tree("./static/", "./www/static")

# create homepage
sorted_posts = sorted(posts, key=itemgetter('date'), reverse=True) # sort by date
template = Template(filename='./tmpl/homepage.html')
rendered = template.render(info=info, posts=sorted_posts)
# write homepage
with codecs.open("./www/index.html", "w", "utf-8-sig") as temp:        
    temp.write(rendered)
    
# create each post
for post in posts:
    pre = markdown(post["content"]) # preprocessed markdown
    p_path = './www/' + post["file"]
    os.mkdir(p_path)
    template = Template(filename='./tmpl/post.html') # an Mako's Template object
    rendered = template.render(content=pre, post=post, info=info) # a rendered post
    # write post
    with codecs.open(p_path + "/index.html", "w", "utf-8-sig") as temp:        
        temp.write(rendered)

print("Done!")