from bible_guesser.bible import Bible

if __name__ == "__main__":
    bible = Bible()
    print([book.title for book in bible.books])
    print([chapter.number for chapter in bible.books[0].chapters])
    print([verse.number for verse in bible.books[0].chapters[0].verses])
    print(bible.books[0].chapters[0].verses[30].text)
