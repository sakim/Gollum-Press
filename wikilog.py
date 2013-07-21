from dateutil import parser
from flask import Flask, request, redirect, url_for
from flask.templating import render_template
from werkzeug.contrib.atom import AtomFeed
from post import Post
from post_list import PostList

app = Flask(__name__)
app.config.from_pyfile('config.cfg')


@app.route('/')
def index():
    return redirect(url_for('get_posts'))


@app.route('/posts', methods=['GET'])
def get_posts():
    page = int(request.args.get('page', '1'))
    postList = PostList(page,
                        working_dir=app.config['REPOSITORY'],
                        index=app.config['INDEX_PAGE'],
                        per_page=app.config['POSTS_PER_PAGE'])
    return render_template('post_list.html', posts=postList.posts, page=page)


@app.route('/posts/<path:post_id>', methods=['GET'])
def get_post(post_id):
    post = Post(post_id, working_dir=app.config['REPOSITORY'])
    return render_template('post.html', post=post)


@app.route('/atom.xml', methods=['GET'])
def get_feed():
    postList = PostList(1,
                        working_dir=app.config['REPOSITORY'],
                        index=app.config['INDEX_PAGE'],
                        per_page=app.config['POSTS_PER_PAGE'])
    feed = AtomFeed(app.config['TITLE'], feed_url=request.url, url=request.url_root)
    for post in postList.posts:
        date = parser.parse(post.date)
        feed.add(post.title, post.content_markup,
                 id=post.post_id,
                 content_type='html',
                 author=post.author,
                 url=u"posts/{0}".format(post.post_id),
                 updated=date,
                 published=date)

    return feed.get_response()

if __name__ == '__main__':
    app.run(debug=True)
