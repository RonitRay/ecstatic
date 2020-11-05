import os
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown

POSTS = {}

for markdown_post in os.listdir('content'):
    file_path = os.path.join('content', markdown_post)

    with open(file_path, 'r') as file:
        POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])

    
POSTS = {
    post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%d-%m-%Y'), reverse=True)
}

env = Environment(loader=PackageLoader('generate', 'templates'))
home_template = env.get_template('home.html')
post_template = env.get_template('post.html')

posts_metadata = [POSTS[post].metadata for post in POSTS]
tags = [];
for post in posts_metadata:
    if post['blog']=='yes':
        tags.extend(post['tags'].split(', '));
tags=list(set(tags));
tags.sort();

tag_template = env.get_template('tag.html')
for tag in tags:
    tagposts_metadata = [POSTS[post].metadata for post in POSTS if tag in POSTS[post].metadata['tags'].split(', ')]
    tag_html = tag_template.render(tagposts=tagposts_metadata, tag=tag)
    with open('output/posts/tag-'+tag+'.html', 'w') as file:
        file.write(tag_html)
        

home_html = home_template.render(posts=posts_metadata, tags=tags)

with open('output/index.html', 'w') as file:
    file.write(home_html)

for post in POSTS:
    post_metadata = POSTS[post].metadata

    post_data = {
        'content': POSTS[post],
        'title': post_metadata['title'],
        'date': post_metadata['date'],
        'blog': post_metadata['blog']
    }

    post_html = post_template.render(post=post_data)
    post_file_path = 'output/posts/{slug}.html'.format(slug=post_metadata['slug'])

    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as file:
        file.write(post_html)

