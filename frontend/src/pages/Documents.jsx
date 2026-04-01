import { useState, useEffect } from 'react';
import axios from 'axios';
import { FileText, Cpu, Trash2, Upload, Plus, AlertCircle, CheckCircle, Database } from 'lucide-react';

export default function Documents() {
  const [documents, setDocuments] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [uploadData, setUploadData] = useState({ title: '', company_name: '', document_type: 'invoice', file: null });

  const fetchDocuments = async () => {
    try {
      const res = await axios.get('http://localhost:8000/documents');
      setDocuments(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    if (!uploadData.file) return;
    setIsUploading(true);
    
    const formData = new FormData();
    formData.append('title', uploadData.title);
    formData.append('company_name', uploadData.company_name);
    formData.append('document_type', uploadData.document_type);
    formData.append('file', uploadData.file);

    try {
      await axios.post('http://localhost:8000/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setShowUploadModal(false);
      fetchDocuments();
      setUploadData({ title: '', company_name: '', document_type: 'invoice', file: null });
    } catch (err) {
      console.error(err);
      alert('Upload failed: ' + (err.response?.data?.detail || err.message));
    } finally {
      setIsUploading(false);
    }
  };

  const handleIndex = async (id) => {
    try {
      await axios.post(`http://localhost:8000/rag/index-document?document_id=${id}`);
      fetchDocuments();
    } catch (err) {
      console.error(err);
      alert('Indexing failed: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleDelete = async (id) => {
    if (!confirm('Are you sure you want to delete this document?')) return;
    try {
      await axios.delete(`http://localhost:8000/documents/${id}`);
      fetchDocuments();
    } catch (err) {
      console.error(err);
      alert('Delete failed');
    }
  };

  return (
    <div className="animate-fade-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
        <div>
          <h1 style={{ fontSize: '2rem', marginBottom: '8px' }}>Asset Vault</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Manage and analyze incoming financial documents.</p>
        </div>
        <button className="btn-primary" onClick={() => setShowUploadModal(true)}>
          <Plus size={20} /> Ingest File
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '24px' }}>
        {documents.map((doc) => (
          <div key={doc.id} className="glass-card" style={{ padding: '24px', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '16px' }}>
              <div style={{ padding: '12px', background: 'rgba(14, 165, 233, 0.1)', borderRadius: '12px' }}>
                <FileText size={24} color="var(--accent-color)" />
              </div>
              {doc.is_indexed ? (
                <span className="badge" style={{ display: 'flex', alignItems: 'center', gap: '4px', background: 'rgba(16, 185, 129, 0.1)', color: '#10b981', borderColor: 'rgba(16, 185, 129, 0.3)' }}>
                  <CheckCircle size={12} /> Embedded
                </span>
              ) : (
                <span className="badge" style={{ display: 'flex', alignItems: 'center', gap: '4px', background: 'rgba(245, 158, 11, 0.1)', color: '#f59e0b', borderColor: 'rgba(245, 158, 11, 0.3)' }}>
                  <AlertCircle size={12} /> Pending Index
                </span>
              )}
            </div>
            
            <h3 style={{ fontSize: '1.1rem', marginBottom: '4px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{doc.title}</h3>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '20px' }}>{doc.company_name} • {doc.document_type}</p>
            
            <div style={{ display: 'flex', gap: '8px', marginTop: 'auto' }}>
              <button 
                onClick={() => handleIndex(doc.id)} 
                disabled={doc.is_indexed}
                className="btn-secondary" 
                style={{ flex: 1, padding: '8px', fontSize: '0.85rem', opacity: doc.is_indexed ? 0.5 : 1 }}
              >
                <Cpu size={16} /> {doc.is_indexed ? 'Vectorized' : 'Run Vector RAG'}
              </button>
              <button 
                onClick={() => handleDelete(doc.id)}
                className="btn-secondary"
                style={{ padding: '8px', color: '#ef4444', borderColor: 'rgba(239, 68, 68, 0.3)' }}
                title="Delete"
              >
                <Trash2 size={16} />
              </button>
            </div>
          </div>
        ))}

        {documents.length === 0 && (
          <div style={{ gridColumn: '1 / -1', padding: '60px', textAlign: 'center', color: 'var(--text-secondary)', background: 'var(--bg-glass)', borderRadius: '16px', border: '1px dashed var(--border-glass)' }}>
            <Database size={48} style={{ opacity: 0.5, marginBottom: '16px' }} />
            <h3>No documents found in the vault</h3>
            <p style={{ marginTop: '8px' }}>Upload a securely formatted PDF or TXT to get started.</p>
          </div>
        )}
      </div>

      {/* Upload Modal */}
      {showUploadModal && (
        <div style={{ position: 'fixed', inset: 0, background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(8px)', zIndex: 100, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <div className="glass-panel animate-fade-in" style={{ width: '100%', maxWidth: '500px', padding: '32px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
              <h2 style={{ fontSize: '1.5rem', margin: 0 }}>Ingest New Document</h2>
              <button 
                onClick={() => setShowUploadModal(false)}
                style={{ background: 'transparent', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer' }}
              >
                ✕
              </button>
            </div>
            
            <form onSubmit={handleUpload}>
              <div className="form-group">
                <label className="form-label">Document Title</label>
                <input required type="text" className="input-glass" value={uploadData.title} onChange={e => setUploadData({...uploadData, title: e.target.value})} placeholder="e.g. Q3 Earnings Report" />
              </div>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '20px' }}>
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Context / Company</label>
                  <input required type="text" className="input-glass" value={uploadData.company_name} onChange={e => setUploadData({...uploadData, company_name: e.target.value})} placeholder="e.g. Acme Corp" />
                </div>
                
                <div className="form-group" style={{ marginBottom: 0 }}>
                  <label className="form-label">Document Type</label>
                  <select className="input-glass" value={uploadData.document_type} onChange={e => setUploadData({...uploadData, document_type: e.target.value})} style={{ appearance: 'none', background: 'rgba(0,0,0,0.4)' }}>
                    <option value="report">Annual Report</option>
                    <option value="invoice">Invoice</option>
                    <option value="contract">Legal Contract</option>
                    <option value="other">Other Asset</option>
                  </select>
                </div>
              </div>

              <div className="form-group" style={{ marginBottom: '32px' }}>
                <label className="form-label">Binary File (PDF/TXT)</label>
                <div style={{ padding: '24px', border: '2px dashed var(--border-glass)', borderRadius: '12px', textAlign: 'center', background: 'rgba(0,0,0,0.2)' }}>
                  <input 
                    required type="file" 
                    onChange={e => setUploadData({...uploadData, file: e.target.files[0]})}
                    style={{ width: '100%', color: 'var(--text-primary)' }}
                    accept=".pdf,.txt"
                  />
                </div>
              </div>

              <div style={{ display: 'flex', gap: '16px', justifyContent: 'flex-end' }}>
                <button type="button" className="btn-secondary" onClick={() => setShowUploadModal(false)}>Cancel</button>
                <button type="submit" className="btn-primary" disabled={isUploading}>
                  {isUploading ? 'Processing...' : <><Upload size={18} /> Ingest to Vault</>}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
