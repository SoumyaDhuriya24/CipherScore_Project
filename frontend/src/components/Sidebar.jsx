import './Sidebar.css';

const Sidebar = ({ ciphers, selectedCipher, onSelectCipher, rounds, onRoundsChange }) => {
    return (
        <div className="sidebar-sections">
            {/* Cipher Selection */}
            <div className="sidebar-section">
                <h3 className="sidebar-section-title">Algorithms</h3>
                <div className="cipher-list">
                    {ciphers.map((cipher) => (
                        <button
                            key={cipher.id}
                            onClick={() => onSelectCipher(cipher.id)}
                            className={`cipher-button ${selectedCipher === cipher.id ? 'cipher-button-active' : ''}`}
                        >
                            <div className={`cipher-indicator ${selectedCipher === cipher.id ? 'cipher-indicator-active' : ''}`} />
                            {cipher.name}
                        </button>
                    ))}
                </div>
            </div>

            {/* Configuration */}
            <div className="sidebar-section">
                <h3 className="sidebar-section-title">Configuration</h3>
                <div className="config-panel">
                    <label className="config-label">
                        Avalanche Test Rounds
                    </label>
                    <div className="slider-labels">
                        <span>100</span>
                        <span className="slider-value">{rounds}</span>
                        <span>5000</span>
                    </div>
                    <input
                        type="range"
                        min="100"
                        max="5000"
                        step="100"
                        value={rounds}
                        onChange={(e) => onRoundsChange(parseInt(e.target.value))}
                        className="slider"
                    />
                </div>
            </div>
        </div>
    );
};

export default Sidebar;
