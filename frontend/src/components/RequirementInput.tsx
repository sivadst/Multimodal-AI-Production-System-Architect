import React, { useState } from 'react';

export const RequirementInput = ({ onSubmit }: { onSubmit: (text: string, image?: string) => void }) => {
    const [text, setText] = useState('');
    const [image, setImage] = useState<string | undefined>(undefined);

    const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (ev) => {
                setImage(ev.target?.result as string);
            };
            reader.readAsDataURL(file);
        }
    };

    return (
        <div style={{ padding: '20px', border: '1px solid #ccc', margin: '10px' }}>
            <h2>Requirements Input</h2>
            <textarea 
                value={text} 
                onChange={(e) => setText(e.target.value)} 
                rows={5} 
                cols={50} 
                placeholder="Enter system requirements..." 
            />
            <br />
            <input type="file" accept="image/*" onChange={handleImageUpload} />
            <br />
            {image && <img src={image} alt="Preview" style={{ maxWidth: '200px' }} />}
            <br />
            <button onClick={() => onSubmit(text, image)}>Design Architecture</button>
        </div>
    );
};
