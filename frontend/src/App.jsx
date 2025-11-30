/**
 * @fileoverview Main Application Component for SuperShredder
 * 
 * This is the root component that orchestrates the entire single-page application.
 * It assembles all major sections (Hero, Preview, Features, etc.) into a cohesive
 * scrollable landing page experience.
 * 
 * @author Team PD Lovers
 * @version 1.0.0
 */

import React from 'react';

// Layout Components
import Navbar from './components/Navbar';
import Footer from './components/Footer';

// Page Section Components
import HeroSection from './pages/HeroSection';
import FeaturesGrid from './pages/FeaturesGrid';
import TechSpecs from './pages/TechSpecs';
import AppPreview from './components/AppPreview';
import GuidePage from './pages/GuidePage';
import DownloadPage from './pages/DownloadPage';
import ContactPage from './pages/ContactPage';

/**
 * Root Application Component
 * 
 * Renders the complete SuperShredder landing page with all sections.
 * Uses a dark slate theme with smooth scroll navigation between sections.
 * 
 * @returns {JSX.Element} The complete application layout
 */
function App() {
    return (
        <div className="min-h-screen bg-slate-950 text-slate-200 selection:bg-red-500/30">
            <Navbar />

            <main>
                {/* Landing Area */}
                <section id="hero">
                    <HeroSection />
                </section>

                {/* The Desktop Simulator - Key Feature */}
                <section id="preview" className="relative z-10 -mt-10">
                    <AppPreview />
                </section>

                {/* Technical Details */}
                <section id="features">
                    <FeaturesGrid />
                </section>

                <section id="specs">
                    <TechSpecs />
                </section>

                {/* Documentation */}
                <section id="guide" className="bg-slate-900/50">
                    <GuidePage />
                </section>

                {/* Action Areas */}
                <section id="download">
                    <DownloadPage />
                </section>

                <section id="contact">
                    <ContactPage />
                </section>
            </main>

            <Footer />
        </div>
    );
}

export default App;