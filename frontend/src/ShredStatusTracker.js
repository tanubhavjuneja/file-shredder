// ShredStatusTracker.js (Create this file)

import React, { useState, useEffect } from 'react';
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api/',
});

const ShredStatusTracker = ({ taskId }) => {
  const [status, setStatus] = useState('PENDING');
  const [message, setMessage] = useState('Task queued...');
  const [percent, setPercent] = useState(0);
  const [isFinished, setIsFinished] = useState(false);

  useEffect(() => {
    if (!taskId || isFinished) return;

    // Polling function runs every 3 seconds
    const interval = setInterval(async () => {
      try {
        const response = await api.get(`shred/status/${taskId}/`);
        const data = response.data;
        
        // Update general status
        setStatus(data.status);

        if (data.status === 'PROGRESS' && data.progress_data) {
          setMessage(data.progress_data.status_message);
          setPercent(data.progress_data.percent || 0);
        }

        if (data.ready) {
          clearInterval(interval);
          setIsFinished(true);
          // Set final status and message from the result object
          const finalResult = data.result;
          setStatus(finalResult.status.toUpperCase());
          setMessage(finalResult.message);
          setPercent(100);
        }
      } catch (error) {
        clearInterval(interval);
        setStatus('CONNECTION ERROR');
        setMessage('Could not connect to the backend status API.');
        setIsFinished(true);
      }
    }, 3000); 

    return () => clearInterval(interval);
  }, [taskId, isFinished]);

  if (!taskId) {
    return null;
  }
  
  const progressStyle = {
      color: isFinished ? (status === 'SUCCESS' ? 'green' : 'red') : 'orange'
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: '15px', marginTop: '20px' }}>
      <h3>Shredding Task Status: <span style={progressStyle}>{status}</span></h3>
      <p>Task ID: {taskId}</p>
      
      <div style={{ width: '100%', backgroundColor: '#eee', borderRadius: '4px' }}>
        <div style={{ 
          width: `${percent}%`, 
          backgroundColor: progressStyle.color, 
          height: '25px', 
          textAlign: 'right',
          paddingRight: '5px',
          color: 'white',
          lineHeight: '25px',
          borderRadius: '4px'
        }}>
          {percent.toFixed(1)}%
        </div>
      </div>

      <p>Details: {message}</p>
    </div>
  );
};

export default ShredStatusTracker;