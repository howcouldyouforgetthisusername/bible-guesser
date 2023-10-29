import React, { useState } from 'react';
import './App.css';

function App() {
  const [verse, setVerse] = useState('Random verse will appear here.');

  // This function could be used to get the verse from your Flask API
  const fetchVerse = () => {
    fetch('http://localhost:5000/api/random_verse')
      .then(response => response.json())
      .then(data => {
        console.log('Received data:', data); // Log the received data for inspection
        setVerse(data.verse_text); // Assuming the response has a 'text' field with the verse
      })
      .catch(error => {
        console.error('Error fetching verse:', error);
      });
  };


  return (
    <div className="App">
      <header className="App-header">
        <h1>BibleGuesser</h1>
        <button onClick={fetchVerse}>Get Random Verse</button>
        <p>{verse}</p>
        {/* Add more UI components here as needed */}
      </header>
    </div>
  );
}

export default App;
