import React from 'react';

export const CodePreview = ({ code }: { code: Record<string, string> }) => {
    return (
        <div style={{ padding: '20px', border: '1px solid #ccc', margin: '10px' }}>
            <h2>Generated Code Preview</h2>
            {Object.entries(code).map(([filename, content]) => (
                <div key={filename} style={{ marginBottom: '20px' }}>
                    <h3>{filename}</h3>
                    <pre style={{ backgroundColor: '#1e1e1e', color: '#d4d4d4', padding: '10px', overflowX: 'auto' }}>
                        {content}
                    </pre>
                </div>
            ))}
        </div>
    );
};
