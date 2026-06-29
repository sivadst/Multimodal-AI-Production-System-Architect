import React from 'react';

export const ServiceEditor = ({ services }: { services: any[] }) => {
    return (
        <div style={{ padding: '20px', border: '1px solid #ccc', margin: '10px' }}>
            <h2>Service Details</h2>
            {services.map((svc, idx) => (
                <div key={idx} style={{ marginBottom: '15px' }}>
                    <h4>{svc.name}</h4>
                    <p><strong>Responsibility:</strong> {svc.responsibility}</p>
                    <p><strong>Owner:</strong> {svc.owner_team}</p>
                    <ul>
                        {svc.endpoints?.map((ep: any, i: number) => (
                            <li key={i}>{ep.method} {ep.path} - {ep.summary}</li>
                        ))}
                    </ul>
                </div>
            ))}
        </div>
    );
};
