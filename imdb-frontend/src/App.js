import React, { useState } from 'react';
import Login from './components/Login';
import MovieSearch from './components/MovieSearch';
import PersonSearch from './components/PersonSearch';

const App = () => {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem('token'));
  const [view, setView] = useState('movies');

  if (!loggedIn) return <Login onLogin={() => setLoggedIn(true)} />;

  return (
    <div>
      <nav style={{ padding: '1rem', background: '#eee' }}>
        <button onClick={() => setView('movies')}>Movie Search</button>
        <button onClick={() => setView('people')}>Person Search</button>
        <button onClick={() => { localStorage.clear(); setLoggedIn(false); }}>Logout</button>
      </nav>
      {view === 'movies' && <MovieSearch />}
      {view === 'people' && <PersonSearch />}
    </div>
  );
};

export default App;
