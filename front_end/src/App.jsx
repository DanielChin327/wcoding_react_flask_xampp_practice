// Import necessary modules and components
import React, { useState } from 'react';         // React library and useState hook for state management
import axios from 'axios';                       // Axios library for making HTTP requests
import ShowQuotes from './components/ShowQuotes';// Custom component to display quotes
import './App.css';                              // Import CSS styles for the App component

// Define the main App component
function App() {
  // Declare state variables using the useState hook
  const [personName, setPersonName] = useState('');    // State to hold the person's name input
  const [quote, setQuote] = useState('');              // State to hold the quote input
  const [message, setMessage] = useState('');          // State to hold messages to display to the user
  const [refreshQuotes, setRefreshQuotes] = useState(false); // State to trigger refreshing the quotes list

  // Function to handle saving a new quote
  const handleSave = async () => {
    try {
      // Send a POST request to the backend API with the new quote data
      const response = await axios.post('http://localhost:5000/api/quote', {
        person_name: personName,  // Include the person's name in the request body
        quote: quote,             // Include the quote text in the request body
      });

      // Update the message state with the success message from the response
      setMessage(response.data.message);

      // Clear the input fields by resetting the state variables
      setPersonName('');
      setQuote('');

      // Toggle the refreshQuotes state to trigger re-fetching the quotes in ShowQuotes component
      setRefreshQuotes((prev) => !prev);
    } catch (error) {
      // If there's an error, update the message state with an error message
      setMessage('Error saving the quote');

      // Log the error to the console for debugging purposes
      console.error(error);
    }
  };

  // Render the component's UI
  return (
    // Main container with className "App" for styling purposes
    <div className="App">
      {/* Heading of the application */}
      <h1>Save Famous Quotes</h1>


      {/* Input field for the person's name */}
      <input
        type="text"                            // Specifies that this is a text input field
        placeholder="Person's Name"            // Placeholder text displayed when the input is empty
        value={personName}                     // Binds the input value to the personName state variable
        onChange={(e) => setPersonName(e.target.value)} // Updates personName state when input changes
      />

      {/* Textarea for the quote */}
      <textarea
        placeholder="Famous Quote"             // Placeholder text displayed when the textarea is empty
        value={quote}                          // Binds the textarea value to the quote state variable
        onChange={(e) => setQuote(e.target.value)} // Updates quote state when textarea content changes
      />

      {/* Button to save the new quote */}
      <button className="save-button" onClick={handleSave}>
        Save Quote
      </button>

      {/* Paragraph to display messages to the user */}
      <p>{message}</p>

      {/* Component to display the list of quotes */}
      <ShowQuotes refresh={refreshQuotes} />   {/* Passes refreshQuotes state as a prop to ShowQuotes */}


    </div>
  );
}

// Export the App component as the default export
export default App;
