# -*- coding: utf-8 -*-
import sys, os
import urllib
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from dateutil import parser
from flask import Flask, request, redirect, url_for, abort
from flask.templating import render_template
from werkzeug.contrib.atom import AtomFeed
from posts import Posts

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

# config
working_dir = app.config['REPOSITORY']
index_page = app.config['INDEX_PAGE']
posts_per_page = app.config['POSTS_PER_PAGE']
theme = app.config['THEME']
site_url = app.config['SITE_URL']

posts = Posts(working_dir=working_dir,
              index=index_page,
              per_page=posts_per_page)


@app.route('/')
def index():
    return redirect(url_for('get_posts'))


@app.route('/posts', methods=['GET'])
def get_posts():
    page = int(request.args.get('page', '1'))

    path = u"{0}/{1}.md".format(working_dir, index_page)
    if not os.path.exists(path):
        abort(500)

    posts.refresh()

    return render_template(u"{0}/post_list.html".format(theme),
                           posts=posts.get_posts(page), recent=posts.get_recent_metas(),
                           page=page, total_pages=posts.get_num_of_pages())


@app.route('/posts/<path:post_id>', methods=['GET'])
def get_post(post_id):
    posts.refresh()
    post = posts.get_post(post_id)
    if post is None:
        abort(404)

    return render_template(u"{0}/post.html".format(theme),
                           post=post, recent=posts.get_recent_metas())


@app.route('/atom.xml', methods=['GET'])
def get_feed():
    feed = AtomFeed(app.config['TITLE'], feed_url=request.url, url=request.url_root)
    posts.refresh()

    for post in posts.get_posts(1):
        date = parser.parse(post.date)
        escaped = urllib.quote(post.post_id.encode("utf-8"))
        url = u"{0}/posts/{1}".format(site_url, escaped)

        feed.add(post.title, post.content_markup.unescape(),
                 id=url,
                 content_type='html',
                 author=post.author,
                 url=url,
                 updated=date,
                 published=date)

    return feed.get_response()


@app.errorhandler(404)
def page_not_found(error):
    posts.refresh()
    return render_template(u"{0}/404.html".format(theme), recent=posts.get_recent_metas()), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template(u"{0}/500.html".format(theme)), 404


if __name__ == '__main__':
    app.run(debug=True)
