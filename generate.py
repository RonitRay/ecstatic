#imports below.

import os
from datetime import datetime, date
import time
from jinja2 import Environment, PackageLoader
from markdown2 import markdown
import json

#a dict to store your posts
POSTS = {}

for markdown_post in os.listdir('content'):
    file_path = os.path.join('content', markdown_post)
    
    # convert from markdown to html and store output in POSTS
    with open(file_path, 'r') as file:
        POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])

# terribly hacky logic to sort it in reverse chronological order
POSTS = {
    post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%d-%b-%Y'), reverse=True)
}

env = Environment(loader=PackageLoader('generate', 'templates'))
home_template = env.get_template('home.html')
post_template = env.get_template('post.html')

# generate pages for each post

for post in POSTS:
    post_metadata = POSTS[post].metadata

    # the next few lines remove miscellaneous characters to replace them with whitespaces
    # a word count is performed to then calculate reading time in post_data.
    post_clean = POSTS[post]
    for char in '-.,\n':
        post_clean = post_clean.replace(char, ' ')
    post_clean = post_clean.lower()

    post_words = post_clean.split()

    post_data = {
        'content': POSTS[post],
        'title': post_metadata['title'],
        'date': post_metadata['date'],
        'blog': post_metadata['blog'],
        'readtime': round(len(post_words)/200)
    }

    post_html = post_template.render(post=post_data)
    post_file_path = 'output/posts/{slug}.html'.format(
        slug=post_metadata['slug'])

    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as file:
        file.write(post_html)

# get post metadata like title, tags, slug etc.
posts_metadata = [POSTS[post].metadata for post in POSTS]

# extract unique list of tags and sort
tags = []
for post in posts_metadata:
    if post['blog'] == 'yes':
        tags.extend(post['tags'].split(', '))
tags = list(set(tags))
tags.sort()

# make a list of posts for each tag, then create a new page dedicated to all posts for that tag
tag_template = env.get_template('tag.html')
for tag in tags:
    tagposts_metadata = [
        POSTS[post].metadata for post in POSTS if tag in POSTS[post].metadata['tags'].split(', ')]
    tag_html = tag_template.render(tagposts=tagposts_metadata, tag=tag)
    with open('output/posts/tag-'+tag+'.html', 'w') as file:
        file.write(tag_html)

# renders the index.html homepage by passing all relevant data to the template
home_html = home_template.render(posts=posts_metadata, tags=tags, activities=activities, updated=updated)

with open('output/index.html', 'w') as file:
    file.write(home_html)
### add your patches below ###

# end
