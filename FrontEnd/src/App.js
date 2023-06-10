import './App.css';

import HomePage from './pages/HomePage';
import UploadPage from './pages/UploadPage';
import StreamPage from './pages/StreamPage';
import { BrowserRouter as Router, Route,Routes } from 'react-router-dom';

function App() {
  return (
   

      <Router>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/stream" element={<StreamPage />} />
        </Routes>
      </Router>
    
  );
}

export default App;
