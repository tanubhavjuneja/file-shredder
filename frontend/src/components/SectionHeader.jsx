/**
 * @fileoverview Section Header Component
 * 
 * A reusable header component for page sections that provides
 * consistent typography and styling across all major sections.
 * 
 * @author Team PD Lovers
 * @version 1.0.0
 */

import React from 'react';

/**
 * Section Header Component
 * 
 * Renders a styled header with title, optional subtitle, and decorative underline.
 * Used to introduce major sections of the landing page.
 * 
 * @param {Object} props - Component props
 * @param {string} props.title - The main heading text
 * @param {string} [props.subtitle] - Optional descriptive text below the title
 * @param {boolean} [props.centered=true] - Whether to center-align the header
 * @returns {JSX.Element} A styled section header
 * 
 * @example
 * <SectionHeader 
 *   title="Features" 
 *   subtitle="Explore what makes SuperShredder unique" 
 * />
 */
export default function SectionHeader({ title, subtitle, centered = true }) {
    return (
        <div className={`mb-12 ${centered ? 'text-center' : 'text-left'}`}>
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-4 tracking-tight">
                {title}
            </h2>
            {subtitle && (
                <p className="text-lg text-slate-400 max-w-2xl mx-auto">
                    {subtitle}
                </p>
            )}
            <div className={`h-1 w-20 bg-blue-600 rounded mt-6 ${centered ? 'mx-auto' : ''}`}></div>
        </div>
    );
}