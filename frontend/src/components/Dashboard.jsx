import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';
import { TrendingUp, Cpu, Zap, ShieldAlert } from 'lucide-react';
import './Dashboard.css';

const Dashboard = ({ report }) => {
    if (!report) return null;

    const avalancheStr = report['Avalanche Score'] || '0%';
    const avalancheVal = parseFloat(avalancheStr.replace('%', ''));
    const speed = report['Encryption Speed (ms)'] || '0 ms';
    const memory = report['Peak Memory (KB)'] || '0 KB';
    const attackStatus = report['Attack Status'] || 'Not Run';

    const chartData = [
        { name: 'Avalanche Score', value: avalancheVal, target: 50 },
    ];

    const getAvalancheColor = (val) => {
        const diff = Math.abs(val - 50);
        return diff < 5 ? '#10b981' : '#ef4444';
    };

    return (
        <div className="dashboard">
            {/* Metrics Row */}
            <div className="metrics-grid">
                {/* Avalanche */}
                <div className="metric-card">
                    <div className="metric-icon">
                        <TrendingUp style={{ width: 48, height: 48 }} />
                    </div>
                    <div className="metric-content">
                        <p className="metric-label">Avalanche Effect</p>
                        <h3 className="metric-value" style={{ color: getAvalancheColor(avalancheVal) }}>
                            {avalancheStr}
                        </h3>
                    </div>
                    <p className="metric-target">Target: 50% (Ideal Randomness)</p>
                    <div className="progress-bar">
                        <div
                            className="progress-fill"
                            style={{ width: `${avalancheVal}%`, backgroundColor: getAvalancheColor(avalancheVal) }}
                        />
                    </div>
                </div>

                {/* Speed */}
                <div className="metric-card">
                    <div className="metric-icon">
                        <Zap style={{ width: 48, height: 48 }} />
                    </div>
                    <div className="metric-content">
                        <p className="metric-label">Encryption Speed</p>
                        <h3 className="metric-value metric-value-primary">{speed}</h3>
                    </div>
                    <p className="metric-target">Lower is Better</p>
                </div>

                {/* Memory */}
                <div className="metric-card">
                    <div className="metric-icon">
                        <Cpu style={{ width: 48, height: 48 }} />
                    </div>
                    <div className="metric-content">
                        <p className="metric-label">Peak Memory</p>
                        <h3 className="metric-value metric-value-secondary">{memory}</h3>
                    </div>
                    <p className="metric-target">IoT Target: &lt; 10 KB</p>
                </div>

                {/* Attack Status */}
                <div className="metric-card">
                    <div className="metric-icon">
                        <ShieldAlert style={{ width: 48, height: 48 }} />
                    </div>
                    <div className="metric-content">
                        <p className="metric-label">Attack Resistance</p>
                        <h3 className="metric-value metric-value-warning">{attackStatus}</h3>
                    </div>
                    <p className="metric-target">Simulation Result</p>
                </div>
            </div>

            {/* Chart & JSON Row */}
            <div className="analysis-grid">
                {/* Chart */}
                <div className="chart-card">
                    <h4 className="chart-title">
                        <TrendingUp style={{ width: 20, height: 20, color: 'var(--accent-primary)' }} />
                        Visual Analysis
                    </h4>
                    <div className="chart-container">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={chartData} layout="vertical">
                                <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" horizontal={false} />
                                <XAxis type="number" domain={[0, 100]} stroke="var(--text-muted)" />
                                <YAxis type="category" dataKey="name" stroke="var(--text-primary)" width={120} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: 'var(--bg-secondary)', borderColor: 'var(--border-color)', color: 'var(--text-primary)' }}
                                    itemStyle={{ color: 'var(--text-primary)' }}
                                />
                                <Legend />
                                <Bar dataKey="value" name="Current Score" fill="#8884d8" barSize={30}>
                                    {chartData.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={getAvalancheColor(entry.value)} />
                                    ))}
                                </Bar>
                                <Bar dataKey="target" name="Ideal Target (50%)" fill="var(--text-muted)" barSize={5} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* JSON Report */}
                <div className="json-card">
                    <h4 className="chart-title">
                        <Cpu style={{ width: 20, height: 20, color: 'var(--accent-secondary)' }} />
                        Raw Data
                    </h4>
                    <div className="json-container">
                        <pre className="json-content">
                            {JSON.stringify(report, null, 2)}
                        </pre>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
