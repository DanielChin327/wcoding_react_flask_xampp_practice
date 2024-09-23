import {useState} from 'react';
import {useEffect} from 'react';
import './ShowQuotes.css'

function ShowQuotes() {
  const [quotes, setQuotes] = useState([]);

  useEffect(() => {
    const fetchQuotes = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/api/quotes');
        const data = await response.json();
        setQuotes(data)
      }
      catch(error) {
        console.log("Error fetching quotes", error);
      }
    };
    fetchQuotes();

  }, []);

return (
  <>
  <table className="quotes-table">
                <thead>
                    <tr>
                        <th className="quotes-header">Person</th>
                        <th className="quotes-header">Quote</th>
                    </tr>
                </thead>
                <tbody>
                    {quotes.map((quote, index) => (
                        <tr key={index} className="quotes-row">
                            <td className="quotes-personName">{quote.person_name}</td>
                            <td className="quotes-quote">{quote.quote}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
  </>


)

}




export default ShowQuotes
