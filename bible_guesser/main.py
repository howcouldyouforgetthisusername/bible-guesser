from bible_guesser.bible import Bible

if __name__ == "__main__":
    bible = Bible()
    print(list(bible.books.keys()))
    print(list(bible["Exodus"].chapters.keys()))
    print(list(bible["Exodus"][1].verses.keys()))
    print(bible["Exodus"][1][3].text)
