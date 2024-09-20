import React, { useState } from 'react';
import axios from 'axios';
import ShowQuotes from './components/ShowQuotes'


function App() {
  const [personName, setPersonName] = useState('');
  const [quote, setQuote] = useState('');
  const [message, setMessage] = useState('');

  const handleSave = async () => {
    try {
      const response = await axios.post('http://localhost:5000/api/save_quote', {
        person_name: personName,
        quote: quote
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage('Error saving the quote');
      console.error(error);
    }
  };

  return (
    <div className="App">
      <h1>Save Famous Quotes</h1>
      <input
        type="text"
        placeholder="Person's Name"
        value={personName}
        onChange={(e) => setPersonName(e.target.value)}
      />
      <textarea
        placeholder="Famous Quote"
        value={quote}
        onChange={(e) => setQuote(e.target.value)}
      />
      <button onClick={handleSave}>Save Quote</button>
      <p>{message}</p>


      <ShowQuotes></ShowQuotes>




    </div>
  );





}

export default App;
