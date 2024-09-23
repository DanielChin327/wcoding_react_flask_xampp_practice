import { useState, useEffect } from 'react';
import axios from 'axios';
import './ShowQuotes.css';

function ShowQuotes() {
  const [quotes, setQuotes] = useState([]);

  useEffect(() => {
    fetchQuotes();
  }, []);

  // Function to fetch quotes from the backend
  const fetchQuotes = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/api/quotes');
      setQuotes(response.data);
    } catch (error) {
      console.log('Error fetching quotes', error);
    }
  };

  // Function to handle deletion of a quote
  const handleDelete = async (quote_id) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/api/quote/${quote_id}`);
      // Remove the deleted quote from the state
      setQuotes(quotes.filter((quote) => quote.quotes_id !== quote_id)); // This deletes without needing to refresh
    } catch (error) {
      console.log('Error deleting quote', error);
    }
  };

  return (
    <>
      <table className="quotes-table">
        <thead>
          <tr>
            <th className="quotes-header">Person</th>
            <th className="quotes-header">Quote</th>
            <th className="quotes-header">Delete</th>
          </tr>
        </thead>
        <tbody>
          {quotes.map((quote) => (
            <tr key={quote.quotes_id} className="quotes-row">
              <td className="quotes-personName">{quote.person_name}</td>
              <td className="quotes-quote">{quote.quote}</td>
              <td className="quotes-actions">
                <button className = "delete-button" onClick={() => handleDelete(quote.quotes_id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

export default ShowQuotes;
