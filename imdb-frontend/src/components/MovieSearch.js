import React, { useState } from 'react';
import api from '../services/api';

const MovieSearch = () => {
  const [filters, setFilters] = useState({ title: '', year: '', genre: '', type: '' });
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const res = await api.get('/search/movie', { params: filters });
      setResults(res.data || []);
    } catch (err) {
      alert('Failed to fetch movies');
    }
  };

  return (
    <div style={{ padding: '1rem' }}>
      <h2>🎬 Movie Search</h2>
      <input placeholder="Title" onChange={e => setFilters(f => ({ ...f, title: e.target.value }))} />
      <input placeholder="Year" onChange={e => setFilters(f => ({ ...f, year: e.target.value }))} />
      <input placeholder="Genre" onChange={e => setFilters(f => ({ ...f, genre: e.target.value }))} />
      <input placeholder="Type" onChange={e => setFilters(f => ({ ...f, type: e.target.value }))} />
      <button onClick={handleSearch}>Search</button>

      <div style={{ marginTop: '1rem', display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' }}>
        {results.map((r, i) => (
          <div key={i} style={{ border: '1px solid #ccc', padding: '1rem' }}>
            <h3>{r['Title']}</h3>
            <p><strong>Year:</strong> {r['Year Released']}</p>
            <p><strong>Type:</strong> {r['Type']}</p>
            <p><strong>Genre:</strong> {r['Genre']}</p>
            <p><strong>People:</strong></p>
            <ul>
              {(r['List of People Associated'] || []).map((p, j) => <li key={j}>{p}</li>)}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MovieSearch;
