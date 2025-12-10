import type { SidebarsConfig } from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
    tutorialSidebar: [
        'intro',
        {
            type: 'category',
            label: 'Chapter 1: Introduction to RAG',
            items: [
                'chapter-1/what-is-rag',
                'chapter-1/why-rag-matters',
                'chapter-1/prerequisites',
            ],
        },
        {
            type: 'category',
            label: 'Chapter 2: Core Concepts',
            items: [
                'chapter-2/vector-embeddings',
                'chapter-2/similarity-search',
                'chapter-2/context-augmentation',
            ],
        },
        {
            type: 'category',
            label: 'Chapter 3: Implementation',
            items: [
                'chapter-3/building-pipeline',
                'chapter-3/tools-libraries',
                'chapter-3/best-practices',
            ],
        },
        {
            type: 'category',
            label: 'Chapter 4: Advanced Topics',
            items: [
                'chapter-4/optimization',
                'chapter-4/applications',
                'chapter-4/resources',
            ],
        },
        {
            type: 'category',
            label: 'Chapter 5: AI Safety & Ethics',
            items: ['chapter-5/ai-safety', 'chapter-5/ethics'],
        },
    ],
};

export default sidebars;
