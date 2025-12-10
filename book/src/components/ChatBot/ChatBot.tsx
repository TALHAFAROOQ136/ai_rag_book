import React, { useState, useEffect, useRef } from 'react';
import './ChatBot.css';

interface Message {
    role: 'user' | 'assistant';
    content: string;
    sources?: Source[];
}

interface Source {
    page_title: string;
    page_url: string;
    section: string;
    relevance_score: number;
}

interface ChatBotProps {
    apiUrl?: string;
    initialQuestion?: string;
    isOpen?: boolean;
    onClose?: () => void;
}

export const ChatBot: React.FC<ChatBotProps> = ({
    apiUrl = 'http://localhost:8000',
    initialQuestion = '',
    isOpen = false,
    onClose
}) => {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState(initialQuestion);
    const [isLoading, setIsLoading] = useState(false);
    const [isChatOpen, setIsChatOpen] = useState(isOpen);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    // Auto-scroll to bottom
    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Handle initial question
    useEffect(() => {
        if (initialQuestion && isChatOpen) {
            setInput(initialQuestion);
            handleSubmit(new Event('submit') as any, initialQuestion);
        }
    }, [initialQuestion, isChatOpen]);

    // Handle streaming response
    const handleStreamingResponse = async (question: string) => {
        const response = await fetch(`${apiUrl}/api/chat/stream`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question,
                top_k: 5
            }),
        });

        if (!response.body) {
            throw new Error('No response body');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let assistantMessage = '';
        let sources: Source[] = [];

        // Add placeholder message
        setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));

                        if (data.type === 'token') {
                            assistantMessage += data.token;
                            // Update message in real-time
                            setMessages(prev => {
                                const newMessages = [...prev];
                                newMessages[newMessages.length - 1] = {
                                    role: 'assistant',
                                    content: assistantMessage
                                };
                                return newMessages;
                            });
                        } else if (data.type === 'sources') {
                            sources = data.sources;
                        } else if (data.type === 'done') {
                            // Add sources to final message
                            setMessages(prev => {
                                const newMessages = [...prev];
                                newMessages[newMessages.length - 1] = {
                                    role: 'assistant',
                                    content: assistantMessage,
                                    sources
                                };
                                return newMessages;
                            });
                        }
                    } catch (e) {
                        console.error('Error parsing stream data:', e);
                    }
                }
            }
        }
    };

    const handleSubmit = async (e: React.FormEvent, questionOverride?: string) => {
        e.preventDefault();
        const question = questionOverride || input;

        if (!question.trim()) return;

        // Add user message
        setMessages(prev => [...prev, { role: 'user', content: question }]);
        setInput('');
        setIsLoading(true);

        try {
            await handleStreamingResponse(question);
        } catch (error) {
            console.error('Error:', error);
            setMessages(prev => [
                ...prev,
                {
                    role: 'assistant',
                    content: 'Sorry, there was an error processing your request. Please make sure the backend is running.'
                }
            ]);
        } finally {
            setIsLoading(false);
        }
    };

    const toggleChat = () => {
        setIsChatOpen(!isChatOpen);
        if (!isChatOpen && inputRef.current) {
            setTimeout(() => inputRef.current?.focus(), 100);
        }
    };

    const handleClose = () => {
        setIsChatOpen(false);
        if (onClose) onClose();
    };

    return (
        <>
            {/* Chat Toggle Button */}
            {!isChatOpen && (
                <button className="chat-toggle-btn" onClick={toggleChat} aria-label="Open chat">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                </button>
            )}

            {/* Chat Window */}
            {isChatOpen && (
                <div className="chatbot-container">
                    <div className="chatbot-header">
                        <h3>RAG Book Assistant</h3>
                        <button className="close-btn" onClick={handleClose} aria-label="Close chat">
                            ✕
                        </button>
                    </div>

                    <div className="chatbot-messages">
                        {messages.length === 0 && (
                            <div className="welcome-message">
                                <h4>👋 Welcome!</h4>
                                <p>Ask me anything about Retrieval-Augmented Generation!</p>
                                <div className="suggested-questions">
                                    <button onClick={() => setInput("What is RAG?")}>What is RAG?</button>
                                    <button onClick={() => setInput("How do vector embeddings work?")}>How do embeddings work?</button>
                                    <button onClick={() => setInput("What are RAG best practices?")}>Best practices?</button>
                                </div>
                            </div>
                        )}

                        {messages.map((message, index) => (
                            <div key={index} className={`message ${message.role}`}>
                                <div className="message-content">
                                    {message.content}
                                </div>
                                {message.sources && message.sources.length > 0 && (
                                    <div className="message-sources">
                                        <strong>Sources:</strong>
                                        <ul>
                                            {message.sources.map((source, i) => (
                                                <li key={i}>
                                                    <a href={source.page_url} target="_blank" rel="noopener noreferrer">
                                                        {source.page_title}
                                                    </a>
                                                    <span className="relevance-score">
                                                        ({(source.relevance_score * 100).toFixed(0)}% relevant)
                                                    </span>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        ))}

                        {isLoading && (
                            <div className="message assistant loading">
                                <div className="typing-indicator">
                                    <span></span>
                                    <span></span>
                                    <span></span>
                                </div>
                            </div>
                        )}

                        <div ref={messagesEndRef} />
                    </div>

                    <form className="chatbot-input" onSubmit={handleSubmit}>
                        <input
                            ref={inputRef}
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            placeholder="Ask a question about the book..."
                            disabled={isLoading}
                        />
                        <button type="submit" disabled={isLoading || !input.trim()}>
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                                <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            </svg>
                        </button>
                    </form>
                </div>
            )}
        </>
    );
};
