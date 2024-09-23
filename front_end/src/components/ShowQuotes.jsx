import { useState, useEffect } from 'react';
import axios from 'axios';
import './ShowQuotes.css';

function ShowQuotes({ refresh }) {
  const [quotes, setQuotes] = useState([]);
  const [editingQuoteId, setEditingQuoteId] = useState(null);
  const [editPersonName, setEditPersonName] = useState('');
  const [editQuoteText, setEditQuoteText] = useState('');

  useEffect(() => {
    fetchQuotes();
  }, [refresh]);

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
      setQuotes(quotes.filter((quote) => quote.quotes_id !== quote_id));
    } catch (error) {
      console.log('Error deleting quote', error);
    }
  };

  // Function to handle editing of a quote
  const handleEditClick = (quote) => {
    setEditingQuoteId(quote.quotes_id);
    setEditPersonName(quote.person_name);
    setEditQuoteText(quote.quote);
  };

  // Function to handle updating a quote
  const handleUpdate = async (quote_id) => {
    try {
      await axios.put(`http://127.0.0.1:5000/api/quote/${quote_id}`, {
        person_name: editPersonName,
        quote: editQuoteText,
      });
      // Update the quotes list
      setQuotes(
        quotes.map((quote) =>
          quote.quotes_id === quote_id
            ? { ...quote, person_name: editPersonName, quote: editQuoteText }
            : quote
        )
      );
      // Reset editing state
      setEditingQuoteId(null);
      setEditPersonName('');
      setEditQuoteText('');
    } catch (error) {
      console.log('Error updating quote', error);
    }
  };

  // Function to handle canceling the edit
  const handleCancelEdit = () => {
    setEditingQuoteId(null);
    setEditPersonName('');
    setEditQuoteText('');
  };

  return (
    <>
      <table className="quotes-table">
        <thead>
          <tr>
            <th className="quotes-header">Person</th>
            <th className="quotes-header">Quote</th>
            <th className="quotes-header">Actions</th>
          </tr>
        </thead>
        <tbody>
          {quotes.map((quote) => (
            <tr key={quote.quotes_id} className="quotes-row">
              <td className="quotes-personName">
                {editingQuoteId === quote.quotes_id ? (
                  <input
                    type="text"
                    value={editPersonName}
                    onChange={(e) => setEditPersonName(e.target.value)}
                  />
                ) : (
                  quote.person_name
                )}
              </td>
              <td className="quotes-quote">
                {editingQuoteId === quote.quotes_id ? (
                  <textarea
                    value={editQuoteText}
                    onChange={(e) => setEditQuoteText(e.target.value)}
                  />
                ) : (
                  quote.quote
                )}
              </td>
              <td className="quotes-actions">
                {editingQuoteId === quote.quotes_id ? (
                  <>
                    <button
                      className="save-button"
                      onClick={() => handleUpdate(quote.quotes_id)}
                    >
                      Save
                    </button>
                    <button className="cancel-button" onClick={handleCancelEdit}>
                      Cancel
                    </button>
                  </>
                ) : (
                  <>
                    <button
                      className="edit-button"
                      onClick={() => handleEditClick(quote)}
                    >
                      Edit
                    </button>
                    <button
                      className="delete-button"
                      onClick={() => handleDelete(quote.quotes_id)}
                    >
                      Delete
                    </button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </>
  );
}

export default ShowQuotes;
