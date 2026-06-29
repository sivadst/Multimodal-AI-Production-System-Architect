import React from 'react';

export const ArchitectureCanvas = ({ diagram }: { diagram: string }) => {
    return (
        <div style={{ padding: '20px', border: '1px solid #ccc', margin: '10px' }}>
            <h2>Architecture Diagram</h2>
            <pre style={{ backgroundColor: '#f4f4f4', padding: '10px' }}>{diagram}</pre>
        </div>
    );
};
