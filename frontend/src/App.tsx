import { useState } from 'react';
import { Play, Loader2, AlertCircle } from 'lucide-react';
import './App.css';

function App() {
  const [prompt, setPrompt] = useState('Build a CRM with login, contacts, dashboard, role-based access, and premium plan with payments. Admins can see analytics.');
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const handleGenerate = async () => {
    setIsGenerating(true);
    setError('');
    
    try {
      // Calling your FastAPI backend
      const response = await fetch('https://ai-software-compiler-1.onrender.com/generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ prompt }),
      });

      if (!response.ok) {
        throw new Error(`Server Error: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err: any) {
      setError(err.message || 'Failed to connect to the compilation engine.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div style={{ display: 'flex', height: '100vh', width: '100vw', fontFamily: 'system-ui, sans-serif', backgroundColor: '#0a0a0a', color: '#ededed' }}>
      
      {/* LEFT PANEL: Input & Controls */}
      <div style={{ flex: 1, padding: '2rem', borderRight: '1px solid #333', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        <div>
          <h1 style={{ margin: '0 0 0.5rem 0', fontSize: '1.5rem', fontWeight: 600 }}>AI Software Compiler</h1>
          <p style={{ margin: 0, color: '#888', fontSize: '0.9rem' }}>Multi-stage generation pipeline with deterministic schema enforcement.</p>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', flex: 1 }}>
          <label style={{ fontSize: '0.875rem', fontWeight: 500, color: '#aaa' }}>System Intent Prompt</label>
          <textarea 
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            style={{ 
              flex: 1, padding: '1rem', borderRadius: '8px', backgroundColor: '#1a1a1a', 
              color: '#fff', border: '1px solid #333', resize: 'none', fontSize: '1rem',
              fontFamily: 'monospace'
            }}
            placeholder="Describe the software you want to build..."
          />
        </div>

        <button 
          onClick={handleGenerate}
          disabled={isGenerating || !prompt}
          style={{
            padding: '1rem', backgroundColor: isGenerating ? '#333' : '#fff', color: isGenerating ? '#888' : '#000',
            border: 'none', borderRadius: '8px', fontWeight: 600, cursor: isGenerating ? 'not-allowed' : 'pointer',
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem', fontSize: '1rem', transition: 'all 0.2s'
          }}
        >
          {isGenerating ? <Loader2 style={{ animation: 'spin 1s linear infinite' }} size={20} /> : <Play size={20} />}
          {isGenerating ? 'Compiling Schema...' : 'Run Compiler'}
        </button>

        {error && (
          <div style={{ padding: '1rem', backgroundColor: '#4a0f0f', color: '#ffb3b3', borderRadius: '8px', display: 'flex', gap: '0.5rem', alignItems: 'flex-start' }}>
            <AlertCircle size={20} style={{ flexShrink: 0 }} />
            <p style={{ margin: 0, fontSize: '0.9rem' }}>{error}</p>
          </div>
        )}
      </div>

      {/* RIGHT PANEL: Output Viewer */}
      <div style={{ flex: 1, padding: '2rem', display: 'flex', flexDirection: 'column', overflow: 'hidden', backgroundColor: '#111' }}>
        <h2 style={{ margin: '0 0 1rem 0', fontSize: '1rem', fontWeight: 500, color: '#aaa' }}>Strict Configuration Output</h2>
        
        <div style={{ flex: 1, overflowY: 'auto', backgroundColor: '#000', borderRadius: '8px', border: '1px solid #222', padding: '1.5rem' }}>
          {result ? (
            <pre style={{ margin: 0, color: '#10b981', fontSize: '0.85rem', whiteSpace: 'pre-wrap' }}>
              {JSON.stringify(result, null, 2)}
            </pre>
          ) : (
            <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#444' }}>
              <p>Output will appear here. No manual fixes required.</p>
            </div>
          )}
        </div>
      </div>

    </div>
  );
}

export default App;
