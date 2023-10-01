import re
from typing import Optional

from bible_guesser.loader import read_kjv_text

FIRST_BOOK = "Genesis"
BOOK_TITLES = {
    "The First Book of Moses: Called Genesis": "Genesis",
    "The Second Book of Moses: Called Exodus": "Exodus",
    "The Third Book of Moses: Called Leviticus": "Leviticus",
    "The Fourth Book of Moses: Called Numbers": "Numbers",
    "The Fifth Book of Moses: Called Deuteronomy": "Deuteronomy",
    "The Book of Joshua": "Joshua",
    "The Book of Judges": "Judges",
    "The Book of Ruth": "Ruth",
    "The First Book of Samuel": "1 Samuel",
    "The Second Book of Samuel": "2 Samuel",
    "The First Book of the Kings": "1 Kings",
    "The Second Book of the Kings": "2 Kings",
    "The First Book of the Chronicles": "1 Chronicles",
    "The Second Book of the Chronicles": "2 Chronicles",
    "Ezra": "Ezra",
    "The Book of Nehemiah": "Nehemiah",
    "The Book of Esther": "Esther",
    "The Book of Job": "Job",
    "The Book of Psalms": "Psalms",
    "The Proverbs": "Proverbs",
    "Ecclesiastes": "Ecclesiastes",
    "The Song of Solomon": "Song of Solomon",
    "The Book of the Prophet Isaiah": "Isaiah",
    "The Book of the Prophet Jeremiah": "Jeremiah",
    "The Lamentations of Jeremiah": "Lamentations",
    "The Book of the Prophet Ezekiel": "Ezekiel",
    "The Book of Daniel": "Daniel",
    "Hosea": "Hosea",
    "Joel": "Joel",
    "Amos": "Amos",
    "Obadiah": "Obadiah",
    "Jonah": "Jonah",
    "Micah": "Micah",
    "Nahum": "Nahum",
    "Habakkuk": "Habakkuk",
    "Zephaniah": "Zephaniah",
    "Haggai": "Haggai",
    "Zechariah": "Zechariah",
    "Malachi": "Malachi",
    "The Gospel According to Saint Matthew": "Matthew",
    "The Gospel According to Saint Mark": "Mark",
    "The Gospel According to Saint Luke": "Luke",
    "The Gospel According to Saint John": "John",
    "The Acts of the Apostles": "Acts",
    "The Epistle of Paul the Apostle to the Romans": "Romans",
    "The First Epistle of Paul the Apostle to the Corinthians": "1 Corinthians",
    "The Second Epistle of Paul the Apostle to the Corinthians": "2 Corinthians",
    "The Epistle of Paul the Apostle to the Galatians": "Galatians",
    "The Epistle of Paul the Apostle to the Ephesians": "Ephesians",
    "The Epistle of Paul the Apostle to the Philippians": "Philippians",
    "The Epistle of Paul the Apostle to the Colossians": "Colossians",
    "The First Epistle of Paul the Apostle to the Thessalonians": "1 Thessalonians",
    "The Second Epistle of Paul the Apostle to the Thessalonians": "2 Thessalonians",
    "The First Epistle of Paul the Apostle to Timothy": "1 Timothy",
    "The Second Epistle of Paul the Apostle to Timothy": "2 Timothy",
    "The Epistle of Paul the Apostle to Titus": "Titus",
    "The Epistle of Paul the Apostle to Philemon": "Philemon",
    "The Epistle of Paul the Apostle to the Hebrews": "Hebrews",
    "The General Epistle of James": "James",
    "The First Epistle General of Peter": "1 Peter",
    "The Second General Epistle of Peter": "2 Peter",
    "The First Epistle General of John": "1 John",
    "The Second Epistle General of John": "2 John",
    "The Third Epistle General of John": "3 John",
    "The General Epistle of Jude": "Jude",
    "The Revelation of Saint John the Divine": "Revelation",
}


class Verse:
    text: str
    number: int

    def __init__(self, *, text: str, number: int):
        self.text = text
        self.number = number


class Chapter:
    verses: list[Verse]
    number: int

    def __init__(self, *, number: int, verses: list[Verse]):
        self.number = number
        self.verses = verses


class Book:
    chapters: list[Chapter]
    title: str

    def __init__(self, title: str, text: str):
        self.title = title
        self.chapters = self._load_chapters(text)

    def _load_chapters(self, text: str) -> list[Chapter]:
        curr_chapter = 1
        curr_verse = 1
        chapters: list[Chapter] = []
        while True:
            verses = []
            curr_verse = 1
            while True:
                verse, end_idx = self._get_verse(text, curr_chapter, curr_verse)
                if verse is None:
                    break
                verses.append(verse)
                curr_verse += 1
                if end_idx is not None:
                    text = text[end_idx:]  # Remove the verse we just loaded for efficiency
            if len(verses) == 0:
                break
            chapters.append(Chapter(number=curr_chapter, verses=verses))
            curr_chapter += 1
        return chapters

    def _get_verse(self, text: str, chapter: int, verse: int) -> tuple[Optional[Verse], Optional[int]]:
        pattern = r"(?<!\d)" + str(chapter) + ":" + str(verse) + r"(?!\d)"
        match = re.search(pattern, text)
        if not match:
            return None, None
        verse_start = match.end()
        verse_end_match = re.search(
            r"(?<!\d)" + str(chapter) + r":" + r"(?P<verse>\d+)" + r"(?!\d)",
            text[verse_start + 1 :],
        )
        if verse_end_match:
            verse_end = verse_end_match.start() + verse_start + 1
        else:
            # This is the last verse in the chapter
            next_chapter_start_match = re.search(r"(?<!\d)" + str(chapter + 1) + r":1(?!\d)", text[verse_start + 1 :])
            if next_chapter_start_match:
                verse_end = next_chapter_start_match.start() + verse_start + 1
            else:
                # This is the last verse in the book
                verse_end = None
        verse_text = text[verse_start:verse_end].strip()
        verse_text = re.sub(r"\s+", " ", verse_text)
        return Verse(text=verse_text, number=verse), verse_end


class Bible:
    books: list[Book]
    text: str

    def __init__(self):
        import time

        start_time = time.time()
        self.books = self._load_books(read_kjv_text())
        print(f"Loaded Bible in {time.time() - start_time:.2f} seconds")

    def _load_books(self, text: str) -> list[Book]:
        books = []
        lines = text.splitlines()
        current_book_start_index = 0
        current_book_title = FIRST_BOOK
        for i, line in enumerate(lines):
            if line in BOOK_TITLES:
                books.append(Book(current_book_title, "\n".join(lines[current_book_start_index:i])))
                current_book_start_index = i + 1  # Skip the title line
                current_book_title = BOOK_TITLES[line]
        books.append(Book(current_book_title, "\n".join(lines[current_book_start_index:])))
        return books
