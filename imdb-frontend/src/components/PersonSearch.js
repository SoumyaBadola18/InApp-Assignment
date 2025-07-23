import React, { useState } from 'react';
import api from '../services/api';

const PersonSearch = () => {
  const [filters, setFilters] = useState({ name: '', title: '', profession: '' });
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    try {
      const res = await api.get('/search/person', { params: filters });
      setResults(res.data || []);
    } catch (err) {
      alert('Failed to fetch people');
    }
  };

  return (
    <div style={{ padding: '1rem' }}>
      <h2>🧑 Person Search</h2>
      <input placeholder="Name" onChange={e => setFilters(f => ({ ...f, name: e.target.value }))} />
      <input placeholder="Known For Title" onChange={e => setFilters(f => ({ ...f, title: e.target.value }))} />
      <input placeholder="Profession" onChange={e => setFilters(f => ({ ...f, profession: e.target.value }))} />
      <button onClick={handleSearch}>Search</button>

      <div style={{ marginTop: '1rem', display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1rem' }}>
        {results.map((r, i) => (
          <div key={i} style={{ border: '1px solid #ccc', padding: '1rem' }}>
            <h3>{r.name}</h3>
            <p><strong>Birth Year:</strong> {r.birthYear}</p>
            <p><strong>Profession:</strong> {r.profession}</p>
            <p><strong>Known For:</strong></p>
            <ul>
              {(r.knownForTitles || []).map((t, j) => <li key={j}>{t}</li>)}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PersonSearch;
