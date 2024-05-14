import React from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';

import './App.css';

import HomePage from './pages/Home'
import UserLogin from './pages/UserLogin';

function App() {
  return (
    <Router>
        <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/login" element={<UserLogin />} />
        </Routes>
    </Router>
  );
}

export default App;