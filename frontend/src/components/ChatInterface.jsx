import React, { useState } from 'react';

const ChatInterface = ({ onSendPrompt, response, isLoading, isModelLoaded }) => {
    const [prompt, setPrompt] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (prompt.trim() && !isLoading) {
            onSendPrompt(prompt);
        }
    };

    return (
        <div className="glass-panel chat-interface">
            <div className="response-area">
                {!response && !isLoading && (
                    <div style={{ color: '#94a3b8', textAlign: 'center', paddingTop: '2rem' }}>
                        {isModelLoaded
                            ? "Enter a prompt to analyze the image."
                            : "Waiting for model to load..."}
                    </div>
                )}

                {isLoading && (
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%' }}>
                        <div className="loading-spinner"></div>
                        <span>Processing...</span>
                    </div>
                )}

                {response && (
                    <div style={{ lineHeight: '1.6' }}>
                        <strong style={{ color: '#60a5fa', display: 'block', marginBottom: '0.5rem' }}>Model:</strong>
                        {response}
                    </div>
                )}
            </div>

            <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '1rem' }}>
                <input
                    type="text"
                    className="input-field"
                    placeholder="Ask a question about the image..."
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    disabled={isLoading || !isModelLoaded}
                />
                <button
                    type="submit"
                    className="btn-primary"
                    disabled={isLoading || !prompt.trim() || !isModelLoaded}
                >
                    Send
                </button>
            </form>
        </div>
    );
};

export default ChatInterface;
