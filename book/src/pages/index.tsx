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
        <header className={clsx('hero hero--primary', styles.heroBanner)}>
            <div className="container">
                <Heading as="h1" className="hero__title">
                    {siteConfig.title}
                </Heading>
                <p className="hero__subtitle">{siteConfig.tagline}</p>
                <div className={styles.buttons}>
                    <Link
                        className="button button--secondary button--lg"
                        to="/intro">
                        Start Reading →
                    </Link>
                </div>
            </div>
        </header>
    );
}

export default function Home(): JSX.Element {
    const { siteConfig } = useDocusaurusContext();
    return (
        <Layout
            title={`${siteConfig.title}`}
            description="Learn Retrieval-Augmented Generation with AI-generated content">
            <HomepageHeader />
            <main>
                <section className={styles.features}>
                    <div className="container">
                        <div className="row">
                            <div className={clsx('col col--4')}>
                                <div className="text--center padding-horiz--md">
                                    <h3>📚 Comprehensive Content</h3>
                                    <p>
                                        13 pages covering everything from RAG basics to advanced implementation techniques.
                                    </p>
                                </div>
                            </div>
                            <div className={clsx('col col--4')}>
                                <div className="text--center padding-horiz--md">
                                    <h3>🤖 AI-Powered Chat</h3>
                                    <p>
                                        Ask questions about the book and get instant answers from our RAG-powered chatbot.
                                    </p>
                                </div>
                            </div>
                            <div className={clsx('col col--4')}>
                                <div className="text--center padding-horiz--md">
                                    <h3>🎯 Practical Examples</h3>
                                    <p>
                                        Real-world code examples and best practices you can use immediately.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </section>
            </main>
        </Layout>
    );
}
