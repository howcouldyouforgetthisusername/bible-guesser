import React, { useState } from 'react';
import './App.css';
import bibleData from './bibleData';

// Example static data for books, chapters, and verses
const books = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy']; // Add the rest of the books
const chapters = Array.from({ length: 50 }, (_, i) => i + 1); // Example for 50 chapters
const verses = Array.from({ length: 31 }, (_, i) => i + 1); // Example for 31 verses

function App() {
  const [book, setBook] = useState('');
  const [chapter, setChapter] = useState('');
  const [verse, setVerse] = useState('');
  const [randomVerse, setRandomVerse] = useState('Random verse will appear here.');

  const getChapters = (book) => {
    return Object.keys(bibleData[book].chapters).map(Number);
  };

  const getVerses = (book, chapter) => {
    return Array.from({ length: bibleData[book].chapters[chapter] }, (_, i) => i + 1);
  };

  const handleBookChange = (event) => {
    const newBook = event.target.value;
    setBook(newBook);
    setChapter('');
    setVerse('');
  };

  const handleChapterChange = (event) => {
    const newChapter = event.target.value;
    setChapter(newChapter);
    setVerse('');
  };

  const handleVerseChange = (event) => {
    setVerse(event.target.value);
  };

  // Function to fetch a random verse from your backend
  const fetchRandomVerse = () => {
    fetch('http://localhost:5000/api/random_verse')
      .then(response => response.json())
      .then(data => {
        console.log('Received data:', data); // Log the received data for inspection
        setRandomVerse(data.verse_text); // Update the state with the fetched verse text
      })
      .catch(error => {
        console.error('Error fetching verse:', error);
      });
  };

  const submitGuess = () => {
    // Here you would take the selected book, chapter, and verseNumber and send them to the backend to check the guess
    // For example:
    // fetch('http://localhost:5000/api/check_guess', {
    //   method: 'POST',
    //   headers: {
    //     'Content-Type': 'application/json',
    //   },
    //   body: JSON.stringify({ book, chapter, verseNumber }),
    // })
    // .then(response => response.json())
    // .then(data => {
    //   // Handle the response data - whether the guess was correct or not
    // })
    // .catch(error => {
    //   console.error('Error submitting guess:', error);
    // });
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>BibleGuesser</h1>
        {/* Random Verse Section */}
        <button onClick={fetchRandomVerse}>Get Random Verse</button>
        <p>{randomVerse}</p>
        {/* Book Selection */}
        <select value={book} onChange={handleBookChange}>
          <option value="">Select Book</option>
          {Object.keys(bibleData).map((bookName) => (
            <option key={bookName} value={bookName}>{bookName}</option>
          ))}
        </select>

        {/* Chapter Selection */}
        {book && (
          <select value={chapter} onChange={handleChapterChange}>
            <option value="">Select Chapter</option>
            {getChapters(book).map((chapterNumber) => (
              <option key={chapterNumber} value={chapterNumber}>{chapterNumber}</option>
            ))}
          </select>
        )}

        {/* Verse Selection */}
        {chapter && (
          <select value={verse} onChange={handleVerseChange}>
            <option value="">Select Verse</option>
            {getVerses(book, chapter).map((verseNumber) => (
              <option key={verseNumber} value={verseNumber}>{verseNumber}</option>
            ))}
          </select>
        )}
        <button onClick={submitGuess}>Submit Guess</button>
      </header>
    </div>
  );
}

export default App;