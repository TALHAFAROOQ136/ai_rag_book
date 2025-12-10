import React, { useState } from 'react';
import Root from '@theme-original/Root';
import { ChatBot } from '../components/ChatBot/ChatBot';
import { SelectionMenu } from '../components/SelectionMenu/SelectionMenu';
import { useTextSelection } from '../hooks/useTextSelection';

export default function RootWrapper(props) {
    const [chatOpen, setChatOpen] = useState(false);
    const [initialQuestion, setInitialQuestion] = useState('');

    const { selectedText, position, clearSelection } = useTextSelection(15);

    const handleAskAbout = (text: string) => {
        // Pre-populate chat with selected text
        setInitialQuestion(`Can you explain this: "${text}"`);
        setChatOpen(true);
    };

    return (
        <>
            <Root {...props} />

            {/* Selection Menu - appears when text is selected */}
            <SelectionMenu
                selectedText={selectedText}
                position={position}
                onAskAbout={handleAskAbout}
                onClose={clearSelection}
            />

            {/* ChatBot - always available */}
            <ChatBot
                isOpen={chatOpen}
                initialQuestion={initialQuestion}
                onClose={() => {
                    setChatOpen(false);
                    setInitialQuestion('');
                }}
            />
        </>
    );
}
