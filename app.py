from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.dbconfig import config

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}:{port}/{db}'.format(user=config["user"], pw=config["pwd"],
                                                               url=config["url"], port=config["port"], db=config["db"])
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL  # 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __repr__(self):
        return f"BlogPost{self.id}, title: {self.title};"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/posts/<int:page>", methods=['GET', 'POST'])
def posts(page):
    all_posts = BlogPost.query.all()
    new_offset = (page * 3) - 3
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).limit(3).offset(new_offset).all()
    size = int(len(all_posts) / 3) if len(all_posts) % 3 == 0 else int(len(all_posts) / 3 + 1)
    return render_template('posts.html', posts=posts, size=size, current=page)


@app.route("/do_posts", methods=['POST'])
def do_post():
    post_title = request.form['title']
    post_content = request.form['content']
    post_author = request.form['author']
    new_post = BlogPost(title=post_title, content=post_content, author=post_author)
    db.session.add(new_post)
    db.session.commit()
    return redirect("/posts/1")


@app.route("/search", methods=['GET', 'POST'])
def search():
    title = request.form['search']
    search = "%{}%".format(title)
    posts = BlogPost.query.filter(BlogPost.title.like(search)).all()
    return render_template("search.html", posts=posts)


@app.route("/delete/<int:id>")
def delete(id):
    post_to_delete = BlogPost.query.get_or_404(id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect("/posts/1")


@app.route("/edit/<int:id>", methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == "GET":
        return render_template("edit.html", post=post)
    else:
        # TODO do update here
        post.title = request.form['title']
        post.content = request.form['content']
        post.author = request.form['author']
        post.date_posted = datetime.now()
        db.session.commit()
        return redirect("/posts/1")


@app.route('/home')
def hello_world():
    return '<h1>Hello World!</h1>'


@app.route("/<string:name>")
def greet(name):
    return f"<h1>Hello {name}!</h1>"


@app.route("/users/<string:name>/posts/<int:id>")
def show_post(name, id):
    return f"<h1>Hello {name}, accessing post id: {id}</h1>"


@app.route("/onlyget", methods=["GET"])
def get_req():
    return "This webpage only accepts GET requests"


if __name__ == '__main__':
    app.run(debug=True)
