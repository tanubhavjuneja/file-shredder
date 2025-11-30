/**
 * @fileoverview Application Entry Point
 * 
 * This is the main entry point for the React application.
 * It initializes the React root and renders the App component
 * wrapped in StrictMode for development warnings.
 * 
 * @author Team PD Lovers
 * @version 1.0.0
 */

import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import './index.css';
import App from './App.jsx';

/**
 * Initialize and render the React application.
 * StrictMode enables additional development checks and warnings.
 */
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
