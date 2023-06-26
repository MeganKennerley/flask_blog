from flask import Flask, render_template
import random
from _datetime import datetime as dt
import requests
from post import Post

blog_response = requests.get("https://api.npoint.io/c790b4d5cab58020d391")
blog_json = blog_response.json()
post_objects = []
for post in blog_json:
    post_obj = Post(post["id"], post["title"], post["subtitle"], post["body"])
    post_objects.append(post_obj)

app = Flask(__name__)


@app.route('/')
def blog_home():
    return render_template("index.html", all_posts=post_objects)


@app.route('/post/<int:index>')
def show_posts(index):
    requested_post = None
    for blog_post in post_objects:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.route('/random')
def random_home():
    random_number = random.randint(1, 10)
    current_year = dt.now().date().year
    return render_template("home.html", num=random_number, year=current_year)


@app.route('/guess/<name>')
def guess_name(name):
    params = {
        "name": name
    }
    response = requests.get(url="https://api.agify.io/", params=params)
    response2 = requests.get(url="https://api.genderize.io", params=params)
    return render_template("guess.html", name=response.json()["name"], age=response.json()["age"], gender=response2.json()["gender"])


if __name__ == "__main__":
    app.run(debug=True)
