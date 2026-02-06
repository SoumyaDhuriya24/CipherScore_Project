import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FlaskConical, BookOpen, ShieldCheck, Activity } from 'lucide-react';

const Sidebar = () => {
    const navItems = [
        { icon: LayoutDashboard, label: 'Dashboard', path: '/' },
        { icon: ShieldCheck, label: 'Standard Audit', path: '/audit' },
        { icon: FlaskConical, label: 'Custom Lab', path: '/custom' },
        { icon: BookOpen, label: 'Cipher Library', path: '/library' },
    ];

    return (
        <aside style={{
            width: '280px',
            backgroundColor: 'var(--bg-secondary)',
            borderRight: '1px solid var(--border-light)',
            display: 'flex',
            flexDirection: 'column',
            padding: '1.5rem',
            height: '100%',
            transition: 'width 0.3s ease'
        }}>
            <div style={{ marginBottom: '2.5rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                <Activity size={32} color="var(--primary)" />
                <h1 style={{ fontSize: '1.5rem', fontWeight: 'bold', color: 'var(--text-primary)' }}>CipherScore</h1>
            </div>

            <nav style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                {navItems.map((item) => (
                    <NavLink
                        key={item.path}
                        to={item.path}
                        className={({ isActive }) =>
                            isActive ? 'nav-item active' : 'nav-item'
                        }
                        style={({ isActive }) => ({
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.75rem',
                            padding: '0.875rem 1rem',
                            borderRadius: 'var(--radius-md)',
                            textDecoration: 'none',
                            color: isActive ? 'var(--primary)' : 'var(--text-secondary)',
                            backgroundColor: isActive ? 'var(--primary-light)' : 'transparent',
                            fontWeight: isActive ? '600' : '500',
                            transition: 'all 0.2s'
                        })}
                    >
                        <item.icon size={20} />
                        {item.label}
                    </NavLink>
                ))}
            </nav>

            <div style={{ marginTop: 'auto', padding: '1rem', backgroundColor: 'var(--bg-accent)', borderRadius: 'var(--radius-lg)' }}>
                <p style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
                    <strong>System Status</strong>: Online
                    <br />
                    Backend: Connected
                </p>
            </div>
        </aside>
    );
};

export default Sidebar;
