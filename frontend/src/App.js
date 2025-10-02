

import React, { useState } from 'react';
import ShredForm from './ShredForm'; // Assuming you create ShredForm.js
import ShredStatusTracker from './ShredStatusTracker'; // Assuming you create ShredStatusTracker.js
import './App.css'; 

function App() {
  const [currentTaskId, setCurrentTaskId] = useState(null);

  return (
    <div className="App" style={{ maxWidth: '600px', margin: '50px auto' }}>
      <h1>Secure Shredder Console</h1>
      
      <ShredForm onShredStart={setCurrentTaskId} />
      
      {currentTaskId && <ShredStatusTracker taskId={currentTaskId} />}
      
     
      {currentTaskId && <button onClick={() => setCurrentTaskId(null)}>Start New Task</button>}
    </div>
  );
}

export default App;