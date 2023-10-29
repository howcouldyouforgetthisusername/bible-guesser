import os

from flask import Flask, jsonify
from flask_cors import CORS

import bible_guesser.utils as utils

app = Flask(__name__)
bible = utils.Bible()


# Enable CORS only for development from localhost:3000
app.config["DEBUG"] = os.environ.get("FLASK_ENV") == "development"
if app.config["DEBUG"]:  # Ensure to enable CORS only in development!
    cors = CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.route("/api/random_verse", methods=["GET"])
def random_verse():
    (book, chapter, verse) = utils.get_random_verse(bible)
    return jsonify(
        {
            "book_name": book,
            "chapter_number": chapter,
            "verse_number": verse,
            "verse_text": bible[book][chapter][verse].text,
        }
    )


if __name__ == "__main__":
    app.run()
