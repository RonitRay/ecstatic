import os
from datetime import date

post_title = "title: " + input("Enter title for post: ");

today_date = date.today();
post_date = "date: " + today_date.strftime("%d-%m-%Y");

post_tags = "tags: " + input("Enter a comma-separated list of tags for the post: ");
post_summary = "summary: " + input("Enter a short summary for the post: ");
blog_flag = "blog: " + input("Is this a blog post/do you want it listed on homepage? (yes/no) : ");
filename = input("Enter post slug/shortname: ");
post_slug = "slug: " + filename;

post_template = '---'+'\n';
post_template += post_title + '\n';
post_template += post_date + '\n';
post_template += post_tags + '\n';
post_template += post_summary + '\n';
post_template += blog_flag + '\n';
post_template += post_slug + '\n';
post_template += '---' + '\n';

with open("content/"+filename+".md",'w') as file:
    file.write(post_template)

print('Post generated and placed in content/'+filename+'.md !!!');
