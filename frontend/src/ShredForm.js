import React, { useState } from 'react';
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
  headers: { 'Content-Type': 'application/json' },
});

const ShredFormSync = () => {
  const [targetPath, setTargetPath] = useState('/path/to/file.txt');
  const [passes, setPasses] = useState(7);
  const [chunkSize, setChunkSize] = useState(100);
  const [wipeFree, setWipeFree] = useState(false);
  const [status, setStatus] = useState('Idle');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    // Set processing status immediately
    setStatus('Processing');
    setMessage('Backend is shredding the file...');
    setLoading(true);

    // Use setTimeout to let React render the status before blocking on request
    setTimeout(async () => {
      try {
        const response = await api.post('shred/start/', {
          target_path: targetPath,
          passes: passes,
          chunk_size_mb: chunkSize,
          wipe_free_space: wipeFree ? 'true' : 'false',
        });

        setStatus('Completed');
        setMessage(response.data.message || 'Shredding finished successfully!');
      } catch (error) {
        setStatus('Failed');
        setMessage(error.response?.data?.error || 'Network or unknown error.');
        console.error('Shredding error:', error);
      } finally {
        setLoading(false);
      }
    }, 50); // 50ms delay ensures UI updates first
  };

  return (
    <div style={{ maxWidth: '500px', margin: '20px auto', fontFamily: 'Arial' }}>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        <label>Target Path:</label>
        <input
          type="text"
          value={targetPath}
          onChange={(e) => setTargetPath(e.target.value)}
          placeholder="/path/to/file.txt"
          required
        />

        <label>Passes (min 3):</label>
        <input
          type="number"
          value={passes}
          onChange={(e) => setPasses(parseInt(e.target.value))}
          min="3"
        />

        <label>Chunk Size (MB):</label>
        <input
          type="number"
          value={chunkSize}
          onChange={(e) => setChunkSize(parseInt(e.target.value))}
          min="1"
        />

        <div style={{ display: 'flex', alignItems: 'center' }}>
          <input
            type="checkbox"
            id="wipe-free"
            checked={wipeFree}
            onChange={(e) => setWipeFree(e.target.checked)}
          />
          <label htmlFor="wipe-free" style={{ marginLeft: '5px' }}>Wipe Free Space After?</label>
        </div>

        <button type="submit" disabled={loading} style={{ padding: '8px', cursor: loading ? 'not-allowed' : 'pointer' }}>
          {loading ? 'Processing...' : 'Start Secure Shredding'}
        </button>
      </form>

      <div style={{ marginTop: '20px', padding: '10px', border: '1px solid #ccc', borderRadius: '5px' }}>
        <strong>Status:</strong>{' '}
        <span style={{ color: status === 'Completed' ? 'green' : status === 'Failed' ? 'red' : 'orange' }}>
          {status}
        </span>
        <br />
        <strong>Message:</strong> {message}
      </div>
    </div>
  );
};

export default ShredFormSync;
