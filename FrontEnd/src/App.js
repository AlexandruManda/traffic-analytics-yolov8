import './App.css';

import HomePage from './pages/HomePage';
import StreamPage from './pages/StreamPage';
import { BrowserRouter as Router, Route,Routes } from 'react-router-dom';

function App() {
  return (
   

      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/stream" element={<StreamPage />} />
        </Routes>
      </Router>
    
  );
}

export default App;
