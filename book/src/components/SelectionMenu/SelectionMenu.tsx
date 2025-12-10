import React from 'react';
import './SelectionMenu.css';

interface SelectionMenuProps {
    selectedText: string;
    position: { x: number; y: number } | null;
    onAskAbout: (text: string) => void;
    onClose: () => void;
}

/**
 * Context menu that appears when text is selected
 */
export const SelectionMenu: React.FC<SelectionMenuProps> = ({
    selectedText,
    position,
    onAskAbout,
    onClose
}) => {
    if (!position || !selectedText) return null;

    const handleAsk = () => {
        onAskAbout(selectedText);
        onClose();
    };

    const handleCopy = () => {
        navigator.clipboard.writeText(selectedText);
        onClose();
    };

    return (
        <div
            className="selection-menu"
            style={{
                position: 'absolute',
                left: `${position.x}px`,
                top: `${position.y}px`,
                transform: 'translateX(-50%)'
            }}
        >
            <button
                onClick={handleAsk}
                className="selection-menu-item"
                title="Ask AI about this text"
            >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <circle cx="12" cy="12" r="10" strokeWidth="2" strokeLinecap="round" />
                    <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" strokeWidth="2" strokeLinecap="round" />
                    <line x1="12" y1="17" x2="12.01" y2="17" strokeWidth="2" strokeLinecap="round" />
                </svg>
                Ask about this
            </button>
            <button
                onClick={handleCopy}
                className="selection-menu-item"
                title="Copy to clipboard"
            >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2" strokeWidth="2" />
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" strokeWidth="2" />
                </svg>
                Copy
            </button>
            <button
                onClick={onClose}
                className="selection-menu-close"
                title="Close"
            >
                ✕
            </button>
        </div>
    );
};
