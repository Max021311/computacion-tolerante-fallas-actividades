from prefect import task, flow
import sqlite3
import prefect
import requests
import datetime
import asyncio

DB_NAME = 'activity-6.db'
SETUP_QUERY = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER,
    name TEXT,
    username TEXT,
    street TEXT,
    suite TEXT,
    city TEXT,
    zipcode TEXT,
    lat TEXT,
    lng TEXT,
    phone TEXT,
    website TEXT,
    company_name TEXT,
    company_catch_phrase TEXT,
    company_bs TEXT
);
CREATE INDEX IF NOT EXISTS index_users_id ON users (id);
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER,
    user_id INTEGER,
    title TEXT,
    body TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS index_posts_id ON posts (id);
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER,
    post_id INTEGER,
    name TEXT,
    email TEXT,
    body TEXT,
    FOREIGN KEY(post_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS index_comments_id ON comments (id);
CREATE TABLE IF NOT EXISTS todos (
    id INTEGER,
    user_id INTEGER,
    title TEXT,
    completed INTEGER CHECK (completed IN(0, 1))
);
CREATE INDEX IF NOT EXISTS index_todos_id ON todos (id);
CREATE TABLE IF NOT EXISTS albums (
    id INTEGER,
    user_id INTEGER,
    title TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE INDEX IF NOT EXISTS index_albums_id ON albums (id);
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER,
    album_id INTEGER,
    title TEXT,
    url TEXT,
    thumbnail_url TEXT,
    FOREIGN KEY (album_id) REFERENCES albums(id)
);
CREATE INDEX IF NOT EXISTS index_photos_id ON photos (id);
"""

INSERT_USER_QUERY = """
INSERT INTO users (
    id,
    name,
    username,
    street,
    suite,
    city,
    zipcode,
    lat,
    lng,
    phone,
    website,
    company_name,
    company_catch_phrase,
    company_bs
)
VALUES
(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""
INSERT_POST_QUERY = "INSERT INTO posts (id, user_id, title, body) VALUES (?, ?, ?, ?)"
INSERT_COMMENT_QUERY = "INSERT INTO comments (id, post_id , name , email , body) VALUES (?, ?, ?, ?, ?)"
INSERT_TODO_QUERY = "INSERT INTO todos (id, user_id, title, completed) VALUES (?, ?, ?, ?)"
INSERT_ALBUM_QUERY = "INSERT INTO albums (id, user_id , title) VALUES (?, ?, ?)"
INSERT_PHOTO_QUERY = "INSERT INTO photos (id, album_id, title, url, thumbnail_url) VALUES (?, ?, ?, ?, ?)"

def user_as_tuple(user: dict):
    return (
        user["id"],
        user["name"],
        user["username"],
        user["address"]["street"],
        user["address"]["suite"],
        user["address"]["city"],
        user["address"]["zipcode"],
        user["address"]["geo"]["lat"],
        user["address"]["geo"]["lng"],
        user["phone"],
        user["website"],
        user["company"]["name"],
        user["company"]["catchPhrase"],
        user["company"]["bs"],
    )

def post_as_tuple(post: dict):
    return (post["id"], post["userId"], post["title"], post["body"])

def comment_as_tuple(comment: dict):
    return (comment["id"], comment["postId"], comment["name"], comment["email"], comment["body"])

def todo_as_tuple(todo: dict):
    return (todo["id"], todo["userId"], todo["title"], bool(todo["completed"]))

def album_as_tuple(album: dict):
    return (album["id"], album["userId"], album["title"])

def photo_as_tuple(photo: dict):
    return (photo["id"], photo["albumId"], photo["title"], photo["url"], photo["thumbnailUrl"])

HOST = "https://jsonplaceholder.cypress.io"

@task(name="setup_table")
def setup_table():
    connection = sqlite3.connect(DB_NAME)
    connection.executescript(SETUP_QUERY)
    connection.close()

def get_users() -> list[dict]:
    print('Get users')
    response = requests.get(f"{HOST}/users")
    return response.json()

def get_posts() -> list[dict]:
    print('Get posts')
    response = requests.get(f"{HOST}/posts")
    return response.json()

def get_comments() -> list[dict]:
    print('Get comments')
    response = requests.get(f"{HOST}/comments")
    return response.json()

def get_todos() -> list[dict]:
    print('Get todos')
    response = requests.get(f"{HOST}/todos")
    return response.json()

def get_albums() -> list[dict]:
    print('Get albums')
    response = requests.get(f"{HOST}/albums")
    return response.json()

def get_photos() -> list[dict]:
    print('Get photos')
    response = requests.get(f"{HOST}/photos")
    return response.json()

def on_failure (**kargs):
    print(kargs)
    print('Failed')

def on_completion (**kargs):
    print(kargs)
    print('Completion')

@task(name="get_data", cache_expiration=datetime.timedelta(minutes=5), on_failure=[on_failure], on_completion=[on_completion])
def get_data():
    return {
        "users": get_users(),
        "posts": get_posts(),
        "comments": get_comments(),
        "todos": get_todos(),
        "albums": get_albums(),
        "photos": get_photos(),
    }

@task(name="store_data")
def store_data(data: dict[str, list[dict]]):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    for user in data['users']:
        cursor.execute(INSERT_USER_QUERY, user_as_tuple(user))
    for post in data['posts']:
        cursor.execute(INSERT_POST_QUERY, post_as_tuple(post))
    for comment in data['comments']:
        cursor.execute(INSERT_COMMENT_QUERY, comment_as_tuple(comment))
    for todo in data['todos']:
        cursor.execute(INSERT_TODO_QUERY, todo_as_tuple(todo))
    for album in data['albums']:
        cursor.execute(INSERT_ALBUM_QUERY, album_as_tuple(album))
    for photo in data['photos']:
        cursor.execute(INSERT_PHOTO_QUERY, photo_as_tuple(photo))
    cursor.close()
    connection.commit()
    connection.close()

@flow(log_prints=True)
def my_first_flow():
    setup_table()
    data = get_data()
    store_data(data)
    pass

if __name__ == "__main__":
    asyncio.run(my_first_flow.serve(name="First deploy", interval=datetime.timedelta(seconds=10)))
