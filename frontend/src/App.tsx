import React, { useState } from 'react';
import { RequirementInput } from './components/RequirementInput';
import { ArchitectureCanvas } from './components/ArchitectureCanvas';
import { CodePreview } from './components/CodePreview';
import { TradeoffPanel } from './components/TradeoffPanel';
import { ServiceEditor } from './components/ServiceEditor';

function App() {
    const [design, setDesign] = useState<any>(null);
    const [diagram, setDiagram] = useState<string>('');
    const [code, setCode] = useState<Record<string, string>>({});
    const [loading, setLoading] = useState(false);

    const handleDesignSubmit = async (text: string, image?: string) => {
        setLoading(true);
        try {
            const res = await fetch('/architect/design', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    requirements_text: text,
                    whiteboard_image: image,
                    constraints: {},
                    preferred_patterns: []
                })
            });
            const data = await res.json();
            
            // Generate code for it
            // For real integration we would get an ID back or just pass the full design, 
            // since the API currently expects an ID to retrieve from in-memory DB:
            // But we don't have the ID in the response right now, let's just show the design.
            setDesign(data);
            setDiagram("graph TB\n  Client --> " + data.services?.[0]?.name);
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div style={{ fontFamily: 'sans-serif', maxWidth: '1200px', margin: '0 auto' }}>
            <h1>ArchMind - Multimodal AI Code Architect</h1>
            
            <div style={{ display: 'flex', flexDirection: 'row' }}>
                <div style={{ flex: 1 }}>
                    <RequirementInput onSubmit={handleDesignSubmit} />
                    
                    {loading && <p>Designing architecture...</p>}
                    
                    {design && (
                        <>
                            <TradeoffPanel tradeoffs={design.tradeoffs || []} />
                            <ServiceEditor services={design.services || []} />
                        </>
                    )}
                </div>
                
                <div style={{ flex: 1 }}>
                    {diagram && <ArchitectureCanvas diagram={diagram} />}
                    {Object.keys(code).length > 0 && <CodePreview code={code} />}
                </div>
            </div>
        </div>
    );
}

export default App;
