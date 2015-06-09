import toml, os, codecs, shutil
from operator import itemgetter
from mistune import markdown
from distutils import dir_util
from glob import glob
from mako.template import Template

try:
    with open("config.toml") as cc:
        config = toml.loads(cc.read()) # config dict from TOML file
except Exception as e:
    print("config.toml file not found, copying example config...")
    shutil.copy('config_ex.toml', 'config.toml')
    with open("config.toml") as cc:
        config = toml.loads(cc.read())

posts = []
info = config["info"]

# read files, title and posts content
files = glob('./posts/*.md')
for fiel in files:
    content = open(fiel).read()
    ob = {} # init dict to be inserted after
    f = os.path.basename(fiel) # remove path
    date =  f.split("-")[:3] # removes date from filename
    f_date = '-'.join(date)
    filename = f.replace(f_date, "")[1:].split('.')[0] # extracts filename from path
    # title mode, refer to config.toml
    if info["title_mode"] == "first_only":
        c_title = filename[:1].upper() + filename[1:].replace("-", " ")
    elif info["title_mode"] == "original":
        c_title = filename.replace("-", " ")
    elif info["title_mode"] == "jaden_smith":
        c_title = filename.replace("-", " ").title()

    full = {"content": content, "file": filename, "date": f_date, "title": c_title}
    posts.append(full) # add post to list of posts

if len(posts) < 1:
    print('WARNING: no posts found.')

try:
    shutil.rmtree('./www/') # clean files on www directory
except Exception as e:
    pass # there's no www folder, move on

os.mkdir("./www")
os.mkdir("./www/static")
dir_util.copy_tree("./static/", "./www/static")

# create homepage
sorted_posts = sorted(posts, key=itemgetter('date'), reverse=True) # sort by date
template = Template(filename='./tmpl/homepage.html')
rendered = template.render(info=info, posts=sorted_posts)

with codecs.open("./www/index.html", "w", "utf-8-sig") as temp:
    temp.write(rendered)

# create posts
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
