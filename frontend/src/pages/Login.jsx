import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { ShieldAlert, Fingerprint } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setIsLoading(true);
    
    try {
      await login(username, password);
      navigate('/dashboard/documents');
    } catch (err) {
      setError('Invalid credentials. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container" style={{ alignItems: 'center', justifyItems: 'center', padding: '0 20px', minHeight: '100vh', justifyContent: 'center' }}>
      
      <div className="glass-card animate-fade-in" style={{ width: '100%', maxWidth: '420px', padding: '40px', position: 'relative' }}>
        
        <div style={{ position: 'absolute', top: '-40px', left: '50%', transform: 'translateX(-50%)', 
                      background: 'var(--bg-secondary)', padding: '20px', borderRadius: '50%',
                      boxShadow: 'var(--shadow-glow)', border: '1px solid var(--border-glass)',
                      backdropFilter: 'blur(12px)' }}>
          <Fingerprint size={40} color="var(--accent-color)" />
        </div>

        <div style={{ marginTop: '30px', textAlign: 'center', marginBottom: '32px' }}>
          <h2 style={{ fontSize: '1.5rem', marginBottom: '8px' }}>FinDocs Secure</h2>
          <p style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Authenticate to access intelligence.</p>
        </div>

        {error && (
          <div style={{ background: 'rgba(239, 68, 68, 0.1)', border: '1px solid rgba(239, 68, 68, 0.3)', 
                        color: '#ef4444', padding: '12px', borderRadius: '8px', marginBottom: '20px', 
                        display: 'flex', alignItems: 'center', gap: '8px', fontSize: '0.85rem' }}>
            <ShieldAlert size={16} />
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input 
              type="text" 
              className="input-glass" 
              placeholder="admin" 
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="form-group" style={{ marginBottom: '32px' }}>
            <label className="form-label">Password</label>
            <input 
              type="password" 
              className="input-glass" 
              placeholder="••••••••" 
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          
          <button type="submit" className="btn-primary" style={{ width: '100%', padding: '14px' }} disabled={isLoading}>
            {isLoading ? 'Authenticating...' : 'Secure Login'}
          </button>
        </form>
        
        <div style={{ marginTop: '24px', textAlign: 'center', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
          Unauthorized access is strictly prohibited.
        </div>
      </div>
    </div>
  );
}
