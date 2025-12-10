import { useState, useEffect, useCallback } from 'react';

interface SelectionPosition {
    x: number;
    y: number;
    width: number;
    height: number;
}

interface UseTextSelectionReturn {
    selectedText: string;
    position: SelectionPosition | null;
    clearSelection: () => void;
    isActive: boolean;
}

/**
 * Custom hook to handle text selection in the document
 * 
 * @param minLength - Minimum number of characters to consider a valid selection
 * @returns Selected text, position, and control functions
 */
export const useTextSelection = (
    minLength: number = 10
): UseTextSelectionReturn => {
    const [selectedText, setSelectedText] = useState<string>('');
    const [position, setPosition] = useState<SelectionPosition | null>(null);

    const clearSelection = useCallback(() => {
        setSelectedText('');
        setPosition(null);
        window.getSelection()?.removeAllRanges();
    }, []);

    useEffect(() => {
        const handleSelection = () => {
            const selection = window.getSelection();
            const text = selection?.toString().trim() || '';

            if (text.length >= minLength) {
                setSelectedText(text);

                // Track position for UI placement
                const range = selection?.getRangeAt(0);
                const rect = rect?.getBoundingClientRect();

                if (rect) {
                    setPosition({
                        x: rect.left + rect.width / 2,
                        y: rect.bottom + window.scrollY,
                        width: rect.width,
                        height: rect.height
                    });
                }
            } else {
                clearSelection();
            }
        };

        // Listen to mouseup for selection completion
        document.addEventListener('mouseup', handleSelection);

        // Listen to selectionchange for real-time updates
        document.addEventListener('selectionchange', handleSelection);

        return () => {
            document.removeEventListener('mouseup', handleSelection);
            document.removeEventListener('selectionchange', handleSelection);
        };
    }, [minLength, clearSelection]);

    return {
        selectedText,
        position,
        clearSelection,
        isActive: selectedText.length > 0
    };
};
