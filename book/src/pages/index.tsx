import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';

import styles from './index.module.css';

function HomepageHeader() {
    const { siteConfig } = useDocusaurusContext();
    return (
        <header className={clsx('hero', styles.heroBanner)}>
            <div className="container">
                <div className={styles.heroContent}>
                    <div className={styles.heroText}>
                        <Heading as="h1" className={styles.heroTitle}>
                            {siteConfig.title}
                        </Heading>
                        <p className={styles.heroSubtitle}>
                            Learn <strong>Retrieval-Augmented Generation</strong> through an AI-powered interactive book
                        </p>
                        <p className={styles.heroDescription}>
                            A complete guide covering RAG from fundamentals to advanced implementation,
                            including AI safety and ethics. With 17 pages of AI-generated content and an
                            embedded chatbot that answers your questions in real-time.
                        </p>
                        <div className={styles.buttons}>
                            <Link
                                className="button button--primary button--lg"
                                to="/intro">
                                Start Learning →
                            </Link>
                            <Link
                                className="button button--secondary button--lg"
                                to="/chapter-1/what-is-rag">
                                What is RAG?
                            </Link>
                        </div>
                    </div>
                    <div className={styles.heroImage}>
                        <div className={styles.heroCard}>
                            <div className={styles.cardIcon}>🤖</div>
                            <h3>AI-Powered Learning</h3>
                            <p>Ask questions, get instant answers with citations</p>
                        </div>
                        <div className={styles.heroCard}>
                            <div className={styles.cardIcon}>📚</div>
                            <h3>17 Pages, 5 Chapters</h3>
                            <p>From basics to advanced safety & ethics</p>
                        </div>
                        <div className={styles.heroCard}>
                            <div className={styles.cardIcon}>💡</div>
                            <h3>Practical Examples</h3>
                            <p>Real code you can use immediately</p>
                        </div>
                    </div>
                </div>
            </div>
        </header>
    );
}

function FeatureSection() {
    return (
        <section className={styles.features}>
            <div className="container">
                <div className={styles.sectionHeader}>
                    <Heading as="h2">Why This Book?</Heading>
                    <p>Everything you need to master RAG in one place</p>
                </div>

                <div className="row">
                    <div className={clsx('col col--4')}>
                        <div className={styles.featureCard}>
                            <div className={styles.featureIcon}>📖</div>
                            <h3>Complete Coverage</h3>
                            <p>
                                4 chapters with 13 pages covering vector embeddings, similarity search,
                                context augmentation, and production best practices.
                            </p>
                        </div>
                    </div>

                    <div className={clsx('col col--4')}>
                        <div className={styles.featureCard}>
                            <div className={styles.featureIcon}>🎯</div>
                            <h3>Interactive Learning</h3>
                            <p>
                                Select any text and ask questions about it. Get instant, contextual
                                answers from our RAG-powered chatbot.
                            </p>
                        </div>
                    </div>

                    <div className={clsx('col col--4')}>
                        <div className={styles.featureCard}>
                            <div className={styles.featureIcon}>⚡</div>
                            <h3>Real-Time Streaming</h3>
                            <p>
                                Watch answers appear in real-time with source citations. See exactly
                                where information comes from.
                            </p>
                        </div>
                    </div>
                </div>

                <div className="row" style={{ marginTop: '2rem' }}>
                    <div className={clsx('col col--4')}>
                        <div className={styles.featureCard}>
                            <div className={styles.featureIcon}>💻</div>
                            <h3>Production-Ready Code</h3>
                            <p>
                                20+ code examples using FastAPI, OpenAI, and Qdrant. Copy-paste
                                into your projects.
                            </p>
                        </div>
                    </div>

                    <div className={clsx('col col--4')}>
                        <div className={styles.featureCard}>
                            <div className={styles.featureIcon}>🌙</div>
                            <h3>Dark Mode Support</h3>
                            <p>
                                Read comfortably in any lighting condition with full dark mode
                                support throughout.
                            </p>
                        </div>
                    </div>

                    <div className={clsx('col col--4')}>
                        <div className={styles.featureCard}>
                            <div className={styles.featureIcon}>📱</div>
                            <h3>Mobile Friendly</h3>
                            <p>
                                Fully responsive design. Learn on any device - desktop, tablet,
                                or mobile.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}

function TechStackSection() {
    return (
        <section className={styles.techStack}>
            <div className="container">
                <div className={styles.sectionHeader}>
                    <Heading as="h2">Built With Modern Tech</Heading>
                    <p>Production-grade stack for real-world applications</p>
                </div>

                <div className={styles.techGrid}>
                    <div className={styles.techItem}>
                        <strong>Frontend</strong>
                        <span>Docusaurus 3.0</span>
                    </div>
                    <div className={styles.techItem}>
                        <strong>UI</strong>
                        <span>React 18 + TypeScript</span>
                    </div>
                    <div className={styles.techItem}>
                        <strong>Backend</strong>
                        <span>FastAPI (Python)</span>
                    </div>
                    <div className={styles.techItem}>
                        <strong>LLM</strong>
                        <span>OpenAI GPT-4o-mini</span>
                    </div>
                    <div className={styles.techItem}>
                        <strong>Embeddings</strong>
                        <span>text-embedding-3-small</span>
                    </div>
                    <div className={styles.techItem}>
                        <strong>Vector DB</strong>
                        <span>Qdrant Cloud</span>
                    </div>
                </div>
            </div>
        </section>
    );
}

function ChapterOverview() {
    const chapters = [
        {
            number: 1,
            title: "Introduction to RAG",
            description: "What is RAG, why it matters, and what you need to get started",
            pages: 3,
            link: "/chapter-1/what-is-rag"
        },
        {
            number: 2,
            title: "Core Concepts",
            description: "Vector embeddings, similarity search, and context augmentation",
            pages: 3,
            link: "/chapter-2/vector-embeddings"
        },
        {
            number: 3,
            title: "Implementation",
            description: "Building complete RAG pipelines with best practices",
            pages: 3,
            link: "/chapter-3/building-pipeline"
        },
        {
            number: 4,
            title: "Advanced Topics",
            description: "Optimization, real-world applications, and resources",
            pages: 3,
            link: "/chapter-4/optimization"
        },
        {
            number: 5,
            title: "AI Safety & Ethics",
            description: "Responsible RAG development with safety measures and ethical frameworks",
            pages: 2,
            link: "/chapter-5/ai-safety",
            isNew: true
        }
    ];

    return (
        <section className={styles.chapters}>
            <div className="container">
                <div className={styles.sectionHeader}>
                    <Heading as="h2">What You'll Learn</Heading>
                    <p>A structured path from beginner to advanced</p>
                </div>

                <div className={styles.chapterGrid}>
                    {chapters.map((chapter) => (
                        <Link
                            key={chapter.number}
                            to={chapter.link}
                            className={styles.chapterCard}
                        >
                            <div className={styles.chapterNumber}>
                                Chapter {chapter.number}
                                {chapter.isNew && <span className={styles.newBadge}>NEW</span>}
                            </div>
                            <h3>{chapter.title}</h3>
                            <p>{chapter.description}</p>
                            <div className={styles.chapterMeta}>
                                {chapter.pages} pages →
                            </div>
                        </Link>
                    ))}
                </div>
            </div>
        </section>
    );
}

function CallToAction() {
    return (
        <section className={styles.cta}>
            <div className="container">
                <div className={styles.ctaContent}>
                    <Heading as="h2">Ready to Master RAG?</Heading>
                    <p>
                        Join thousands of developers learning how to build production-ready
                        RAG applications with AI
                    </p>
                    <div className={styles.ctaButtons}>
                        <Link
                            className="button button--primary button--lg"
                            to="/intro">
                            Start Reading Now
                        </Link>
                        <Link
                            className="button button--secondary button--lg"
                            to="https://github.com/TALHAFAROOQ136/ai_rag_book"
                            target="_blank">
                            View on GitHub ⭐
                        </Link>
                    </div>
                </div>
            </div>
        </section>
    );
}

export default function Home(): JSX.Element {
    const { siteConfig } = useDocusaurusContext();
    return (
        <Layout
            title={`${siteConfig.title}`}
            description="Learn Retrieval-Augmented Generation with AI-powered interactive book">
            <HomepageHeader />
            <main>
                <FeatureSection />
                <TechStackSection />
                <ChapterOverview />
                <CallToAction />
            </main>
        </Layout>
    );
}
