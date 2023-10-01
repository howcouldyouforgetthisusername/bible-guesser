import random

from bible_guesser.bible import Bible, Book, Chapter, Verse

VerseReference = tuple[str, int, int]


def get_random_verse(bible: Bible) -> VerseReference:
    """
    Get a random verse from the Bible.
    """
    book = random.choice(list(bible.books.keys()))
    chapter = random.choice(list(bible.books[book].chapters.keys()))
    verse = random.choice(list(bible.books[book].chapters[chapter].verses.keys()))
    return book, chapter, verse


def get_num_verses_off(
    bible: Bible, *, book1: str, chapter1: int, verse1: int, book2: str, chapter2: int, verse2: int
) -> int:
    """
    Get the number of verses between two verses in the Bible.
    """
    verse1_idx = get_unique_verse_index(bible, book1, chapter1, verse1)
    verse2_idx = get_unique_verse_index(bible, book2, chapter2, verse2)
    return abs(verse1_idx - verse2_idx)


def get_unique_verse_index(bible: Bible, book: str, chapter: int, verse: int) -> int:
    """
    Get the index of a verse in the Bible.
    """
    num_verses = 0
    for book_title, book_obj in bible.books.items():
        if book_title != book:
            num_verses += book_obj.num_verses
        else:
            for chapter_number, chapter_obj in book_obj.chapters.items():
                if chapter_number != chapter:
                    num_verses += chapter_obj.num_verses
                else:
                    num_verses += verse
                    break
            break
    return num_verses
