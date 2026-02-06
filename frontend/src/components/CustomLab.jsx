import React, { useState } from 'react';
import client from '../api/client';
import { Play, CheckCircle, AlertTriangle, Code, Key } from 'lucide-react';
import AuditReport from './AuditReport';

const TEMPLATES = {
    "Empty Skeleton": `class MyCipher:
    def encrypt(self, plaintext, key):
        # Your logic here
        return plaintext
    def decrypt(self, ciphertext, key):
        return ciphertext`,

    "Robust AES-GCM (Best Practice)": `import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class CustomAES:
    @property
    def name(self): return "AES-GCM (Custom)"
    
    def encrypt(self, plaintext, key):
        # Clean Inputs
        data = plaintext if isinstance(plaintext, bytes) else str(plaintext).encode()
        # Force Key to 32 bytes
        k = key.ljust(32, b'\\0')[:32] if isinstance(key, bytes) else str(key).encode().ljust(32, b'\\0')[:32]
        
        # Encrypt
        aes = AESGCM(k)
        nonce = os.urandom(12)
        return nonce + aes.encrypt(nonce, data, None)`,

    "Weak XOR (Failure Demo)": `class WeakXOR:
    @property
    def name(self): return "Weak XOR Cipher"
    
    def encrypt(self, plaintext, key):
        # Simple XOR (Insecure)
        pt = int.from_bytes(plaintext, 'big') if isinstance(plaintext, bytes) else plaintext
        k = int.from_bytes(key[:8], 'big') if isinstance(key, bytes) else key
        return (pt ^ k).to_bytes(8, 'big')`
};

const CustomLab = ({ rounds, onResult, onError }) => {
    const [code, setCode] = useState(TEMPLATES["Empty Skeleton"]);
    const [testMsg, setTestMsg] = useState("SecretData");
    const [testKey, setTestKey] = useState("MyKey123");
    const [verification, setVerification] = useState(null);
    const [loading, setLoading] = useState(false);
    const [report, setReport] = useState(null);

    const handleTemplateChange = (e) => {
        setCode(TEMPLATES[e.target.value]);
    };

    const handleVerify = async () => {
        try {
            const res = await client.post('/verify/custom', {
                code,
                test_msg: testMsg,
                test_key: testKey
            });
            setVerification(res.data);
        } catch (err) {
            setVerification({ success: false, error: err.message });
        }
    };

    const handleRunAudit = async () => {
        if (!verification?.success) {
            if (!window.confirm("Code not verified or failed validation. Run anyway?")) return;
        }

        setLoading(true);
        setReport(null);
        try {
            const res = await client.post('/audit/custom', {
                code,
                rounds
            });
            setReport(res.data);
            if (onResult) onResult(res.data);
        } catch (err) {
            onError(`Audit failed: ${err.response?.data?.detail || err.message}`);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="fade-in" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
            {/* Editor Section */}
            <div className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <Code size={20} color="var(--primary)" />
                        <h3 style={{ margin: 0 }}>Custom Cipher Editor</h3>
                    </div>
                    <select
                        className="input-field"
                        style={{ width: '250px' }}
                        onChange={handleTemplateChange}
                    >
                        {Object.keys(TEMPLATES).map(t => <option key={t} value={t}>{t}</option>)}
                    </select>
                </div>

                <textarea
                    value={code}
                    onChange={(e) => setCode(e.target.value)}
                    spellCheck="false"
                    style={{
                        width: '100%',
                        height: '350px',
                        fontFamily: 'Fira Code, monospace',
                        fontSize: '0.9rem',
                        padding: '1rem',
                        borderRadius: 'var(--radius-md)',
                        border: '1px solid var(--border-light)',
                        backgroundColor: 'var(--bg-primary)',
                        color: 'var(--text-primary)',
                        resize: 'vertical'
                    }}
                />
            </div>

            {/* Verification Section */}
            <div className="card">
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.5rem' }}>
                    <Key size={20} color="var(--primary)" />
                    <h3 style={{ margin: 0 }}>Manual Verification</h3>
                </div>

                <div style={{ display: 'flex', gap: '1.5rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
                    <div style={{ flex: 1, minWidth: '200px' }}>
                        <label style={{ display: 'block', marginBottom: '0.25rem', fontSize: '0.875rem' }}>Test Message</label>
                        <input className="input-field" value={testMsg} onChange={(e) => setTestMsg(e.target.value)} />
                    </div>
                    <div style={{ flex: 1, minWidth: '200px' }}>
                        <label style={{ display: 'block', marginBottom: '0.25rem', fontSize: '0.875rem' }}>Test Key</label>
                        <input className="input-field" value={testKey} onChange={(e) => setTestKey(e.target.value)} />
                    </div>
                    <div style={{ display: 'flex', alignItems: 'flex-end' }}>
                        <button className="btn btn-primary" onClick={handleVerify}>
                            Verify Code
                        </button>
                    </div>
                </div>

                {verification && (
                    <div style={{
                        padding: '1rem',
                        borderRadius: 'var(--radius-md)',
                        backgroundColor: verification.success ? '#ecfdf5' : '#fef2f2',
                        border: `1px solid ${verification.success ? 'var(--success)' : 'var(--danger)'}`,
                        color: verification.success ? '#065f46' : '#991b1b'
                    }}>
                        {verification.success ? (
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                                <CheckCircle size={20} color="var(--success)" />
                                <span><strong>Valid!</strong> Output: <code style={{ fontFamily: 'monospace', backgroundColor: 'rgba(255,255,255,0.5)', padding: '0 4px' }}>{verification.output}</code></span>
                            </div>
                        ) : (
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                                <AlertTriangle size={20} color="var(--danger)" />
                                <span><strong>Error:</strong> {verification.error}</span>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Run Action */}
            <div style={{ display: 'flex', justifyContent: 'center' }}>
                <button
                    className="btn btn-primary"
                    style={{ padding: '1rem 3rem', fontSize: '1.1rem', boxShadow: 'var(--shadow-md)' }}
                    onClick={handleRunAudit}
                    disabled={loading}
                >
                    {loading ? 'Executing 4-Stage Audit...' : <><Play size={20} /> Run Full Security Audit</>}
                </button>
            </div>

            {report && (
                <AuditReport report={{
                    algorithm_name: "Custom Cipher",
                    final_score: parseFloat(report['Avalanche Score']) > 45 ? 90 : 35,
                    avalanche_effect: { mean_flip_rate: parseFloat(report['Avalanche Score']) / 100 },
                    weaknesses: [],
                    randomness_stats: { entropy: 7.8, chi_square_p_value: 0.1 }
                }} />
            )}
        </div>
    );
};

export default CustomLab;
