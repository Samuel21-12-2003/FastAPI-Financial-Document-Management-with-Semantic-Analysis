import { NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Files, Search, LogOut, Hexagon } from 'lucide-react';

export default function Sidebar() {
  const { logout, user } = useAuth();
  
  const linkStyle = ({ isActive }) => ({
    textDecoration: 'none',
    padding: '12px 16px',
    borderRadius: '12px',
    display: 'flex',
    alignItems: 'center',
    gap: '12px',
    color: isActive ? 'white' : 'var(--text-secondary)',
    background: isActive ? 'rgba(14, 165, 233, 0.15)' : 'transparent',
    border: '1px solid',
    borderColor: isActive ? 'rgba(14, 165, 233, 0.3)' : 'transparent',
    transition: 'all 0.2s ease',
    fontWeight: 500
  });

  return (
    <div className="sidebar">
      <div style={{ padding: '0 24px', marginBottom: '40px', display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{ padding: '8px', background: 'var(--accent-gradient)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Hexagon color="white" size={24} />
        </div>
        <div>
          <h2 style={{ fontSize: '1.2rem', margin: 0, fontWeight: 700, letterSpacing: '0.5px' }}>FinDocs</h2>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '1px' }}>Enterprise Intel</span>
        </div>
      </div>
      
      <div style={{ padding: '0 16px', display: 'flex', flexDirection: 'column', gap: '8px', flex: 1 }}>
        <NavLink to="/dashboard/documents" style={linkStyle}>
          <Files size={20} /> Documents
        </NavLink>
        <NavLink to="/dashboard/search" style={linkStyle}>
          <Search size={20} /> AI Semantic Search
        </NavLink>
      </div>

      <div style={{ padding: '24px 16px', marginTop: 'auto', borderTop: '1px solid var(--border-glass)' }}>
        <div style={{ marginBottom: '16px', padding: '0 16px', fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span>Role</span>
          <span className="badge">{user?.role || 'Guest'}</span>
        </div>
        <button 
          onClick={logout} 
          style={{ 
            width: '100%', padding: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', 
            gap: '8px', background: 'rgba(239, 68, 68, 0.1)', color: '#ef4444', 
            border: '1px solid rgba(239, 68, 68, 0.3)', borderRadius: '12px', cursor: 'pointer', transition: 'all 0.2s'
          }}
          onMouseOver={(e) => { e.currentTarget.style.background = 'rgba(239, 68, 68, 0.2)' }}
          onMouseOut={(e) => { e.currentTarget.style.background = 'rgba(239, 68, 68, 0.1)' }}
        >
          <LogOut size={18} /> Disconnect Session
        </button>
      </div>
    </div>
  );
}
