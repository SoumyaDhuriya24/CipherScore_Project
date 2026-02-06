import React from 'react';
import { Play, TrendingUp, ShieldAlert, CheckCircle } from 'lucide-react';

const Dashboard = () => {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>

            {/* Hero / Welcome Section */}
            <div className="card" style={{
                background: 'linear-gradient(135deg, var(--primary) 0%, #6366f1 100%)',
                color: 'white',
                border: 'none',
                padding: '2.5rem'
            }}>
                <h1 style={{ color: 'white', marginBottom: '0.5rem' }}>Welcome to CipherScore</h1>
                <p style={{ color: 'rgba(255,255,255,0.9)', maxWidth: '600px', fontSize: '1.1rem' }}>
                    Analyze cryptographic algorithms, visualize avalanche effects, and verify security metrics in real-time.
                </p>
                <button className="btn" style={{
                    marginTop: '1.5rem',
                    backgroundColor: 'white',
                    color: 'var(--primary)',
                    fontWeight: 'bold',
                    border: 'none'
                }}>
                    <Play size={18} /> Start New Audit
                </button>
            </div>

            {/* Stats Grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.5rem' }}>
                <StatCard title="Algorithms Audited" value="12" icon={ShieldAlert} color="var(--primary)" />
                <StatCard title="Avg. Avalanche Effect" value="48.5%" icon={TrendingUp} color="var(--success)" />
                <StatCard title="Tests Passed" value="145" icon={CheckCircle} color="var(--primary)" />
            </div>

            {/* Recent Activity Section */}
            <div className="card">
                <h2 style={{ fontSize: '1.25rem', marginBottom: '1.5rem' }}>Recent Activity</h2>
                <div style={{ overflowX: 'auto' }}>
                    <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
                        <thead>
                            <tr style={{ color: 'var(--text-tertiary)', borderBottom: '1px solid var(--border-light)' }}>
                                <th style={{ padding: '1rem' }}>Algorithm</th>
                                <th style={{ padding: '1rem' }}>Date</th>
                                <th style={{ padding: '1rem' }}>Score</th>
                                <th style={{ padding: '1rem' }}>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <ActivityRow name="Simple XOR" date="Oct 24, 2024" score="12/100" status="Critical" />
                            <ActivityRow name="AES-128" date="Oct 23, 2024" score="98/100" status="Secure" />
                            <ActivityRow name="Custom Feistel" date="Oct 22, 2024" score="65/100" status="Weak" />
                        </tbody>
                    </table>
                </div>
            </div>

        </div>
    );
};

const StatCard = ({ title, value, icon: Icon, color }) => (
    <div className="card" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <div style={{
            padding: '1rem',
            borderRadius: '50%',
            backgroundColor: 'var(--bg-accent)',
            color: color
        }}>
            <Icon size={24} />
        </div>
        <div>
            <p style={{ fontSize: '0.875rem', marginBottom: '0.25rem' }}>{title}</p>
            <h3 style={{ fontSize: '1.5rem', margin: 0 }}>{value}</h3>
        </div>
    </div>
);

const ActivityRow = ({ name, date, score, status }) => {
    const getStatusColor = (s) => {
        if (s === 'Secure') return 'var(--success)';
        if (s === 'Critical') return 'var(--danger)';
        return 'var(--warning)';
    };

    return (
        <tr style={{ borderBottom: '1px solid var(--border-light)' }}>
            <td style={{ padding: '1rem', fontWeight: '500' }}>{name}</td>
            <td style={{ padding: '1rem', color: 'var(--text-secondary)' }}>{date}</td>
            <td style={{ padding: '1rem', fontWeight: 'bold' }}>{score}</td>
            <td style={{ padding: '1rem' }}>
                <span style={{
                    padding: '0.25rem 0.75rem',
                    borderRadius: '1rem',
                    fontSize: '0.75rem',
                    backgroundColor: `${getStatusColor(status)}20`,
                    color: getStatusColor(status),
                    fontWeight: '600'
                }}>
                    {status}
                </span>
            </td>
        </tr>
    );
};

export default Dashboard;
