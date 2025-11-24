import React, { useEffect, useRef } from "react";
import { motion } from "framer-motion";
import "./styles.css";
// FileShredder Page — Full-viewport sections with robust snapping behavior
// Sections: Dashboard, Use Case, Features, Download
// Header & footer fixed. Each section fills the space between header and footer.
// CSS scroll-snap is used where available, and a JS fallback (debounced snap) ensures correct behavior across browsers.

const HEADER_HEIGHT = 72;   // bigger modern header
const FOOTER_HEIGHT = 44;

export default function FileShredderDownloadPage() {
  const sections = [
    { id: "dashboard", title: "Dashboard" },
    { id: "usecase", title: "Use Case" },
    { id: "features", title: "Features" },
    { id: "download", title: "Download" },
  ];

  const containerRef = useRef(null);
  const isSnappingRef = useRef(false);
  const snapTimeoutRef = useRef(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    // Ensure main container height fills area between header & footer
    function setContainerHeight() {
      container.style.height = `calc(100vh - ${HEADER_HEIGHT}px - ${FOOTER_HEIGHT}px)`;
    }
    setContainerHeight();
    window.addEventListener("resize", setContainerHeight);

    // JS fallback snapping: when scrolling stops, snap to the nearest section
    function onScroll() {
      if (isSnappingRef.current) return; // avoid reentrancy
      clearTimeout(snapTimeoutRef.current);
      snapTimeoutRef.current = setTimeout(() => {
        const sectionsEls = Array.from(container.querySelectorAll("section[data-snap]"));
        const containerRectTop = container.getBoundingClientRect().top;

        // Find the section whose center is nearest to container center
        const containerCenter = containerRectTop + container.clientHeight / 2;
        let nearest = sectionsEls[0];
        let nearestDist = Infinity;
        for (const s of sectionsEls) {
          const r = s.getBoundingClientRect();
          const center = r.top + r.height / 2;
          const dist = Math.abs(center - containerCenter);
          if (dist < nearestDist) {
            nearestDist = dist;
            nearest = s;
          }
        }

        if (nearest) {
          isSnappingRef.current = true;
          nearest.scrollIntoView({ behavior: "smooth", block: "start" });
          setTimeout(() => (isSnappingRef.current = false), 600); // allow animation to finish
        }
      }, 80); // small debounce to detect scroll end
    }

    container.addEventListener("scroll", onScroll, { passive: true });

    return () => {
      window.removeEventListener("resize", setContainerHeight);
      container.removeEventListener("scroll", onScroll);
      clearTimeout(snapTimeoutRef.current);
    };
  }, []);

  function scrollTo(id) {
    const container = containerRef.current;
    const el = document.getElementById(id);
    if (!container || !el) return;
    // Use scrollIntoView inside the scrolling container
    el.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  // Common style properties for sections
  const SECTION_BASE_STYLE = {
    height: `calc(100vh - ${HEADER_HEIGHT}px - ${FOOTER_HEIGHT}px)`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
  };


  return (
    <div className="min-h-screen flex flex-col font-sans text-gray-900">
      {/* Fixed Header */}
      <header
        className="fixed top-0 left-0 right-0 z-50 bg-gray-200 backdrop-blur border-b border-gray-300"
        style={{ height: HEADER_HEIGHT }}
      >
        {/* FIX: Use justify-between and w-full to explicitly separate title and buttons */}
        <div className="max-w-7xl mx-auto h-full px-6 flex items-center justify-between w-full">
          {/* Title on the left */}
          <div className="text-xl font-semibold text-gray-800">
            File Shredder
          </div>

          {/* Buttons on the right, ml-auto is removed as justify-between handles spacing */}
          <nav className="flex gap-4">
            {sections.map((s) => (
              <button
                key={s.id}
                onClick={() => scrollTo(s.id)}
                className="px-4 py-2 rounded-lg bg-white border border-gray-300 text-gray-700 hover:bg-gray-100 hover:border-gray-400 transition"
              >
                {s.title}
              </button>
            ))}
          </nav>
        </div>
      </header>



      {/* Main scroll container: uses scroll-snap where supported; JS fallback enforces snapping reliably */}
      <main
        ref={containerRef}
        className="flex-1 overflow-y-auto"
        style={{
          marginTop: HEADER_HEIGHT,
          marginBottom: FOOTER_HEIGHT
        }}
      >
        {/* Dashboard - UNIQUE BACKGROUND */}
        <section id="dashboard" data-snap className="flex items-center justify-center px-6" 
          style={{ ...SECTION_BASE_STYLE, backgroundImage: "url('images/home.jpg')" }}>
          <div className="max-w-4xl text-center text-white">
            <motion.h1 initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className="text-4xl font-bold mb-4">Welcome to File Shredder</motion.h1>
            <p className="text-lg mb-8">
              A simple, secure tool to permanently destroy files. Use the navigation to jump between sections.
            </p>
            <div className="inline-flex gap-3">
              <button onClick={() => scrollTo('usecase')} className="px-6 py-3 rounded-lg bg-white text-gray-900">Use Case</button>
              <button onClick={() => scrollTo('download')} className="px-6 py-3 rounded-lg bg-transparent border border-white text-white">Download</button>
            </div>
          </div>
        </section>

        {/* Use Case - UNIQUE BACKGROUND */}
        <section id="usecase" data-snap className="flex items-center justify-center px-6" 
          style={{ ...SECTION_BASE_STYLE, backgroundImage: "url('images/home.jpg')" }}>
          <div className="max-w-3xl text-center text-white">
            <motion.h2 initial={{ opacity: 0, y: 8 }} whileInView={{ opacity: 1, y: 0 }} className="text-3xl font-semibold mb-4">Why you need a file shredder</motion.h2>
            <p className="leading-relaxed text-lg">
              Regular deletion doesn’t remove the underlying bytes — they can be recovered. File Shredder overwrites files multiple times, encrypts data before destruction, and wipes free space so that files are irrecoverable even with forensic tools.
            </p>
          </div>
        </section>

        {/* Features - UNIQUE BACKGROUND */}
        <section id="features" data-snap className="flex items-center justify-center px-6" 
          style={{ ...SECTION_BASE_STYLE, backgroundImage: "url('images/home.jpg')" }}>
          <div className="max-w-5xl text-white">
            <motion.h2 initial={{ opacity: 0, y: 8 }} whileInView={{ opacity: 1, y: 0 }} className="text-3xl font-semibold text-center mb-8">Features</motion.h2>
            <div className="grid md:grid-cols-3 gap-6">
              <FeatureCard title="Multi-pass Overwrite" desc="Overwrites files with multiple patterns to remove recoverable traces." />
              <FeatureCard title="Encryption Scramble" desc="Locally encrypts file data before destruction for added safety." />
              <FeatureCard title="Free Space Wipe" desc="Scrubs empty disk areas where remnants could remain." />
            </div>
          </div>
        </section>

        {/* Download - UNIQUE BACKGROUND */}
        <section id="download" data-snap className="flex items-center justify-center px-6" 
          style={{ ...SECTION_BASE_STYLE, backgroundImage: "url('images/home.jpg')" }}>
          <div className="max-w-2xl text-center text-white">
            <motion.h2 initial={{ opacity: 0, y: 8 }} whileInView={{ opacity: 1, y: 0 }} className="text-3xl font-semibold mb-4">Download</motion.h2>
            <p className="mb-8">Download the Windows build below. Other platforms coming soon.</p>
            <a href="/shredder.exe" download className="px-8 py-3 rounded-lg bg-white text-gray-900">Download for Windows</a>
          </div>
        </section>
      </main>

      {/* Fixed Footer */}
      <footer className="fixed left-0 right-0 bottom-0 z-50 bg-white/90 backdrop-blur border-t border-gray-200 flex items-center justify-center text-sm text-gray-600" style={{ height: FOOTER_HEIGHT }}>
        © {new Date().getFullYear()} File Shredder — Built for privacy
      </footer>
    </div>
  );
}

function FeatureCard({ title, desc }) {
  return (
    <div className="feature-card">
      {/* FIX: Changed text color for contrast */}
      <h4 className="font-semibold mb-2 text-gray-900">{title}</h4>
      <p className="text-gray-700 text-sm">{desc}</p>
    </div>
  );
}