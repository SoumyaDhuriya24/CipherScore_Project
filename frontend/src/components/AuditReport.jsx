import React from 'react';
import { ShieldCheck, ShieldAlert, BarChart, Activity, Lock } from 'lucide-react';

const AuditReport = ({ report }) => {
    if (!report) return null;

    const getScoreColor = (score) => {
        if (score >= 90) return 'var(--success)';
        if (score >= 70) return 'var(--warning)';
        return 'var(--danger)';
    };

    const score = report.final_score || 0;
    const scoreColor = getScoreColor(score);

    return (
        <div className="card fade-in" style={{ marginTop: '2rem', borderTop: `4px solid ${scoreColor}` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '2rem' }}>
                <div>
                    <h2 style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
                        <ShieldCheck size={28} color={scoreColor} />
                        Security Audit Report
                    </h2>
                    <p style={{ color: 'var(--text-secondary)' }}>
                        Algorithm: <strong>{report.algorithm_name}</strong>
                    </p>
                </div>
                <div style={{ textAlign: 'right' }}>
                    <div style={{ fontSize: '0.875rem', color: 'var(--text-secondary)', marginBottom: '0.25rem' }}>Final Score</div>
                    <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: scoreColor, lineHeight: 1 }}>{score}/100</div>
                </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1.5rem' }}>

                {/* Avalanche Effect */}
                <div style={{ padding: '1.5rem', backgroundColor: 'var(--bg-accent)', borderRadius: 'var(--radius-lg)' }}>
                    <h4 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                        <Activity size={20} /> Avalanche Effect
                    </h4>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                        <span>Bit Flip Rate:</span>
                        <strong>{(report.avalanche_effect?.mean_flip_rate * 100).toFixed(2)}%</strong>
                    </div>
                    <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
                        Ideal is 50%. Measures how changing 1 bit of input affects the output.
                    </p>
                </div>

                {/* Randomness */}
                <div style={{ padding: '1.5rem', backgroundColor: 'var(--bg-accent)', borderRadius: 'var(--radius-lg)' }}>
                    <h4 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                        <BarChart size={20} /> Randomness Stats
                    </h4>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                        <span>Entropy:</span>
                        <strong>{report.randomness_stats?.entropy?.toFixed(4)} / 8.0</strong>
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                        <span>Chi-Square P-Value:</span>
                        <strong>{report.randomness_stats?.chi_square_p_value?.toExponential(2)}</strong>
                    </div>
                </div>

                {/* Attacks Analysis */}
                <div style={{ padding: '1.5rem', backgroundColor: 'var(--bg-accent)', borderRadius: 'var(--radius-lg)' }}>
                    <h4 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                        <Lock size={20} /> Cryptanalysis
                    </h4>
                    <ul style={{ listStyle: 'none', padding: 0 }}>
                        {report.weaknesses?.map((w, i) => (
                            <li key={i} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: 'var(--danger)', marginBottom: '0.5rem' }}>
                                <ShieldAlert size={16} /> {w}
                            </li>
                        ))}
                        {(!report.weaknesses || report.weaknesses.length === 0) && (
                            <li style={{ color: 'var(--success)' }}>No obvious structural weaknesses detected.</li>
                        )}
                    </ul>
                </div>

                {/* Simulated Power Trace (Educational) */}
                {report.power_trace && (
                    <div style={{
                        gridColumn: '1 / -1',
                        padding: '1.5rem',
                        backgroundColor: 'var(--bg-accent)',
                        borderRadius: 'var(--radius-lg)'
                    }}>
                        <h4 style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                            <Activity size={20} /> Simulated Power Side-Channel Trace (Educational)
                        </h4>
                        <div style={{
                            height: '100px',
                            display: 'flex',
                            alignItems: 'flex-end',
                            gap: '2px',
                            borderBottom: '1px solid var(--border-light)',
                            paddingBottom: '4px'
                        }}>
                            {report.power_trace.map((val, i) => (
                                <div key={i} style={{
                                    flex: 1,
                                    height: `${Math.min(100, Math.max(0, val - 30))}%`, // Normalize roughly 40-80 range
                                    backgroundColor: val > 75 ? 'var(--danger)' : 'var(--primary)',
                                    opacity: 0.7,
                                    borderRadius: '1px'
                                }} title={`Sample ${i}: ${val}mV`} />
                            ))}
                        </div>
                        <p style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
                            This is a simulated visualisation of power consumption. Real CPA attacks look for spikes correlated with key bits.
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default AuditReport;
