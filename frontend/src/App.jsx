import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import StandardLibrary from './components/StandardLibrary';
import CustomLab from './components/CustomLab';

// Layout wrapper to apply grid structure
const Layout = ({ children }) => {
  return (
    <div className="layout-container">
      <Sidebar />
      <main className="main-content">
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          {children}
        </div>
      </main>
    </div>
  );
};

const App = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/audit" element={<StandardLibrary rounds={100} onResult={console.log} onError={alert} />} />
          <Route path="/custom" element={<CustomLab rounds={100} onResult={console.log} onError={alert} />} />
          <Route path="/library" element={<div className="card"><h3>Cipher Library</h3><p>Coming soon...</p></div>} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;
