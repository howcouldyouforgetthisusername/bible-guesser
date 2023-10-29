from flask import Flask, jsonify, render_template, request

from bible_guesser import utils
from bible_guesser.bible import Bible

app = Flask(__name__)
bible = Bible()


@app.route("/")
def home():
    title = "Bible Guesser"
    (book, chapter, verse) = utils.get_random_verse(bible)
    return render_template(
        "index.html",
        title=title,
        books=bible.books,
        verse_text=bible[book][chapter][verse].text,
        book=book,
        chapter=chapter,
        verse=verse,
        bible=bible,
    )


@app.route("/guess", methods=["POST"])
def guess():
    guessed_book = request.form.get("book")
    if guessed_book is None:
        raise ValueError("No book guessed")
    guessed_chapter = request.form.get("chapter")
    if guessed_chapter is None:
        raise ValueError("No chapter guessed")
    guessed_chapter = int(guessed_chapter)
    guessed_verse = request.form.get("verse")
    if guessed_verse is None:
        raise ValueError("No verse guessed")
    guessed_verse = int(guessed_verse)
    actual_book = request.form.get("actual_book")
    if actual_book is None:
        raise ValueError("No actual book provided")
    actual_chapter = request.form.get("actual_chapter")
    if actual_chapter is None:
        raise ValueError("No actual chapter provided")
    actual_chapter = int(actual_chapter)
    actual_verse = request.form.get("actual_verse")
    if actual_verse is None:
        raise ValueError("No actual verse provided")
    actual_verse = int(actual_verse)

    correct_guess = False
    if guessed_book == actual_book and guessed_chapter == actual_chapter and guessed_verse == actual_verse:
        correct_guess = True

    num_verses_off = utils.get_num_verses_off(
        bible,
        book1=actual_book,
        chapter1=actual_chapter,
        verse1=actual_verse,
        book2=guessed_book,
        chapter2=guessed_chapter,
        verse2=guessed_verse,
    )

    return render_template(
        "post_guess.html",
        correct_guess=correct_guess,
        book=actual_book,
        chapter=actual_chapter,
        verse=actual_verse,
        num_verses=num_verses_off,
    )


@app.route("/bible", methods=["GET"])
def get_bible():
    return jsonify(bible.to_dict())


if __name__ == "__main__":
    app.run()
