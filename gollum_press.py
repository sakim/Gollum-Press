# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.getcwd())

from dateutil import parser
from flask import Flask, request, redirect, url_for, abort
from flask.templating import render_template
from werkzeug.contrib.atom import AtomFeed
from post import Post
from posts import Posts

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

# config
working_dir = app.config['REPOSITORY']
index_page = app.config['INDEX_PAGE']
posts_per_page = app.config['POSTS_PER_PAGE']
theme = app.config['THEME']


@app.route('/')
def index():
    return redirect(url_for('get_posts'))


@app.route('/posts', methods=['GET'])
def get_posts():
    page = int(request.args.get('page', '1'))

    path = u"{0}/{1}.md".format(working_dir, index_page)
    if not os.path.exists(path):
        abort(500)

    posts = Posts(working_dir=working_dir,
                  index=index_page,
                  per_page=posts_per_page)

    return render_template(u"{0}/post_list.html".format(theme),
                           posts=posts.get_posts(page),
                           recent=posts.get_recent_metas(), page=page, total_pages=posts.get_num_of_pages())


@app.route('/posts/<path:post_id>', methods=['GET'])
def get_post(post_id):
    path = u"{0}/{1}.md".format(working_dir, post_id)
    if not os.path.exists(path):
        abort(404)

    post = Post(post_id, working_dir=working_dir)

    posts = Posts(working_dir=working_dir,
                  index=index_page,
                  per_page=posts_per_page)

    return render_template(u"{0}/post.html".format(theme),
                           post=post, recent=posts.get_recent_metas())


@app.route('/atom.xml', methods=['GET'])
def get_feed():
    posts = Posts(working_dir=working_dir,
                  index=index_page,
                  per_page=posts_per_page)

    feed = AtomFeed(app.config['TITLE'], feed_url=request.url, url=request.url_root)
    for post in posts.get_posts(1):
        date = parser.parse(post.date)
        feed.add(post.title, post.content_markup,
                 id=post.post_id,
                 content_type='html',
                 author=post.author,
                 url=u"/posts/{0}".format(post.post_id),
                 updated=date,
                 published=date)

    return feed.get_response()


@app.errorhandler(404)
def page_not_found(error):
    posts = Posts(working_dir=working_dir,
                  index=index_page,
                  per_page=posts_per_page)
    return render_template(u"{0}/404.html".format(theme), recent=posts.get_recent_metas()), 404


@app.errorhandler(500)
def page_not_found(error):
    return render_template(u"{0}/500.html".format(theme)), 404


if __name__ == '__main__':
    app.run(debug=True)
