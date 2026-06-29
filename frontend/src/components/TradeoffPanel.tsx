import React from 'react';

export const TradeoffPanel = ({ tradeoffs }: { tradeoffs: any[] }) => {
    return (
        <div style={{ padding: '20px', border: '1px solid #ccc', margin: '10px' }}>
            <h2>Architecture Tradeoffs</h2>
            {tradeoffs.map((t, idx) => (
                <div key={idx} style={{ borderBottom: '1px solid #eee', paddingBottom: '10px' }}>
                    <h4>Pattern: {t.pattern}</h4>
                    <p><strong>Latency:</strong> {t.latency_estimation}</p>
                    <p><strong>Cost:</strong> {t.cost_estimation}</p>
                    <p><strong>Complexity:</strong> {t.complexity}</p>
                    <p><strong>Scalability:</strong> {t.scalability}</p>
                    <p><strong>Maintainability:</strong> {t.maintainability}</p>
                    <p><strong>Justification:</strong> {t.justification}</p>
                </div>
            ))}
        </div>
    );
};
