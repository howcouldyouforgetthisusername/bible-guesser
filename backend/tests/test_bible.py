import pytest

from bible_guesser.bible import Bible


@pytest.fixture(scope="module")
def bible_object():
    bible = Bible()
    yield bible


def test_number_of_books(bible_object):
    assert len(bible_object.books) == 66


def test_number_of_chapters(bible_object):
    num_chapters = sum([len(book.chapters) for book in bible_object.books])
    assert num_chapters == 1189


def test_number_of_verses(bible_object):
    num_verses = sum([len(chapter.verses) for book in bible_object.books for chapter in book.chapters])
    assert num_verses == 31102
