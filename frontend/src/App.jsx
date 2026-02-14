import { useState, useEffect } from 'react';
import { getCiphers, runAudit } from './services/api';
import Sidebar from './components/Sidebar';
import CodeEditor from './components/CodeEditor';
import Dashboard from './components/Dashboard';
import { Shield, Activity, Zap } from 'lucide-react';
import './index.css';

function App() {
  const [ciphers, setCiphers] = useState([]);
  const [selectedCipher, setSelectedCipher] = useState(null);
  const [rounds, setRounds] = useState(1000);
  const [customCode, setCustomCode] = useState(defaultCustomCode);
  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadCiphers() {
      try {
        const data = await getCiphers();
        setCiphers(data);
        if (data.length > 0) setSelectedCipher(data[0].id);
      } catch (err) {
        setError("Failed to load ciphers. Is backend running?");
      }
    }
    loadCiphers();
  }, []);

  const handleRunAudit = async () => {
    setLoading(true);
    setError(null);
    setReport(null);
    try {
      const data = await runAudit(selectedCipher, customCode, rounds);
      setReport(data.report);
    } catch (err) {
      setError(err.response?.data?.detail || "Audit failed due to network or server error.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <div className="logo-container">
            <div className="logo-icon">
              <Shield style={{ width: 24, height: 24, color: 'white' }} />
            </div>
            <h1 className="logo-text">CipherScore</h1>
          </div>
          <p className="logo-subtitle">Security Evaluation Suite</p>
        </div>

        <div className="sidebar-content">
          <Sidebar
            ciphers={ciphers}
            selectedCipher={selectedCipher}
            onSelectCipher={setSelectedCipher}
            rounds={rounds}
            onRoundsChange={setRounds}
          />
        </div>

        <div className="sidebar-footer">
          <button
            onClick={handleRunAudit}
            disabled={loading}
            className="btn btn-primary btn-full-width"
          >
            {loading ? (
              <span className="btn-icon">
                <Activity style={{ width: 20, height: 20 }} className="spin" /> Auditing...
              </span>
            ) : (
              <span className="btn-icon">
                <Zap style={{ width: 20, height: 20 }} /> Run Audit
              </span>
            )}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <div className="container space-y-8">
          {error && (
            <div className="alert alert-error">
              <Shield style={{ width: 20, height: 20, color: '#ef4444' }} />
              {error}
            </div>
          )}

          {selectedCipher === 'custom' && (
            <section className="section">
              <div className="section-header">
                <h2 className="section-title">
                  Custom Cipher Implementation
                </h2>
                <span className="section-subtitle">Python 3.x Environment</span>
              </div>
              <div className="card" style={{ padding: 0, overflow: 'hidden', borderColor: 'rgba(139, 92, 246, 0.3)' }}>
                <CodeEditor code={customCode} onChange={setCustomCode} />
              </div>
            </section>
          )}

          {report && (
            <section className="section">
              <Dashboard report={report} />
            </section>
          )}

          {!report && !loading && selectedCipher !== 'custom' && (
            <div className="empty-state">
              <Shield className="empty-state-icon" style={{ width: 64, height: 64 }} />
              <p className="empty-state-text">Select a cipher and run audit to view analytics</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

const defaultCustomCode = `class MyCustomCipher:
    @property
    def name(self):
        return "My Experimental Cipher"

    def encrypt(self, plaintext, key):
        # Example: Simple shift (Caesar) - REPLACE THIS
        # Ensure inputs are ints or bytes
        if isinstance(plaintext, bytes):
            pt_int = int.from_bytes(plaintext, 'big')
            key_int = int.from_bytes(key[:8], 'big')
        else:
            pt_int = plaintext
            key_int = key
            
        # Your Logic Here
        result = pt_int ^ key_int
        return result.to_bytes(8, 'big')

    def decrypt(self, ciphertext, key):
        return ciphertext # Logic here
`;

export default App;
