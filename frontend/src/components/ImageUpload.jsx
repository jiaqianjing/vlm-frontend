import React, { useCallback, useState } from 'react';

const ImageUpload = ({ onImageSelect, selectedImage }) => {
    const [isDragActive, setIsDragActive] = useState(false);

    const handleDrag = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setIsDragActive(true);
        } else if (e.type === 'dragleave') {
            setIsDragActive(false);
        }
    }, []);

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    }, []);

    const handleChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleFile = (file) => {
        if (file.type.startsWith('image/')) {
            onImageSelect(file);
        } else {
            alert("Please upload an image file.");
        }
    };

    return (
        <div className="glass-panel" style={{ height: '100%' }}>
            <div
                className={`upload-zone ${isDragActive ? 'drag-active' : ''}`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => document.getElementById('image-input').click()}
            >
                <input
                    id="image-input"
                    type="file"
                    accept="image/*"
                    onChange={handleChange}
                    style={{ display: 'none' }}
                />

                {selectedImage ? (
                    <div className="preview-container">
                        <img
                            src={URL.createObjectURL(selectedImage)}
                            alt="Preview"
                            className="preview-image"
                        />
                        <p style={{ marginTop: '1rem', color: '#94a3b8' }}>Click or drop to replace</p>
                    </div>
                ) : (
                    <div className="empty-state">
                        <svg
                            width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                            style={{ margin: '0 auto 1rem', color: '#3b82f6' }}
                        >
                            <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
                            <circle cx="8.5" cy="8.5" r="1.5" />
                            <polyline points="21 15 16 10 5 21" />
                        </svg>
                        <h3 style={{ fontSize: '1.25rem', marginBottom: '0.5rem', fontWeight: 600 }}>
                            Upload Image
                        </h3>
                        <p style={{ color: '#94a3b8' }}>
                            Drag and drop or click to select
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default ImageUpload;
