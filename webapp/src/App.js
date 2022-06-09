import { useState } from 'react';
import logo from './logo.svg';
import './App.css';

import { useQuery, gql } from '@apollo/client'

function App() {

  const [limit, setLimit] = useState(3);
  const [offset, setOffset] = useState(0);
  const {
    data,
    loading,
    error
  } = useQuery(gql`
    query Cities($limit: Int, $offset: Int) {
      city(limit: $limit, offset:$offset) {
        name
      }
    }
  `, {
    variables: {
      limit,
      offset,
    },
  });

  return (
    <div className="App">
      <header className="App-header">

      <p>
      Let's visualize some weather data!
      </p>

      <p>Here are some cities...
        (limit:  <input type="number" onChange={e =>  setLimit(e.target.value)} value={limit}/>
         offset: <input type="number" onChange={e => setOffset(e.target.value)} value={offset}/>
        )
      </p>
      {loading
      ? <p>Loading...</p>
      : error
      ? <p>Error :(  {error.message}</p>
      : <ul>
        {data.city.map(city =>
          <li>{city.name}</li>
        )}
      </ul>
      }

        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
