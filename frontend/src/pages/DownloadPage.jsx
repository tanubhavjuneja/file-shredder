/**
 * @fileoverview Download Page Component
 * 
 * Provides download links and information for the SuperShredder application.
 * Includes version info, dependency status, and important warnings.
 * 
 * @author Team PD Lovers
 * @version 1.0.0
 */

import React from 'react';
import { Download, AlertTriangle, Github, Zap, Shield } from 'lucide-react';
import Button from '../components/Button';
import SectionHeader from '../components/SectionHeader';

/**
 * Download Page Component
 * 
 * Renders the download section with:
 * - Version and package information
 * - Dependency status indicator
 * - Direct download and source code buttons
 * - Safety warning about irreversible data destruction
 * 
 * @returns {JSX.Element} The download section
 */
export default function DownloadPage() {
    return (
        <section id="download" className="relative min-h-screen flex flex-col items-center justify-center py-24 bg-slate-950 overflow-hidden">

            {/* Background Grid - Consistent */}
            <div className="absolute inset-0 z-0 opacity-20 pointer-events-none"
                 style={{
                     backgroundImage: 'linear-gradient(#1e293b 1px, transparent 1px), linear-gradient(to right, #1e293b 1px, transparent 1px)',
                     backgroundSize: '40px 40px'
                 }}
            ></div>

            {/* Ambient Glows */}
            <div className="absolute top-1/4 left-1/2 w-[400px] h-[400px] bg-red-600/10 rounded-full blur-[100px] -z-10 pointer-events-none animate-pulse"></div>

            <div className="container mx-auto px-6 text-center relative z-10">
                <SectionHeader title="Get SuperShredder" subtitle="Available for Windows 10/11 (x64) and Android." />

                {/* Main Download Block */}
                <div className="max-w-3xl mx-auto bg-slate-900/50 backdrop-blur-md border border-slate-700 rounded-3xl p-8 md:p-12 mt-12 shadow-2xl shadow-black/50 ring-1 ring-white/5">
                    <div className="flex flex-col items-center">

                        {/* Icon */}
                        <div className="bg-red-600/10 p-5 rounded-full mb-6 border border-red-600/30 shadow-xl shadow-red-900/20">
                            <Download className="w-10 h-10 text-red-500" />
                        </div>

                        <h3 className="text-3xl font-extrabold text-white mb-3 tracking-tight">SuperShredder v1.0.0 (Portable)</h3>
                        <p className="text-slate-400 mb-8 max-w-lg">
                            Pre-packaged standalone executable with bundled necessary ADB binaries for a zero-dependency experience.
                        </p>

                        {/* Dependency Status Panel (Replaced Hash) */}
                        <div className="bg-slate-950/70 border border-slate-800 rounded-xl p-4 w-full max-w-sm mb-8 text-left font-mono shadow-inner">
                            <div className="flex justify-between text-xs text-slate-500 mb-2 border-b border-slate-800 pb-1">
                                <span>STATUS</span>
                                <Zap className="w-4 h-4 text-orange-500" />
                            </div>
                            <div className="text-sm text-slate-300 flex items-center gap-2">
                                <Shield className="w-4 h-4 text-green-500" />
                                Standalone: <span className="text-orange-300 font-bold">Zero Dependencies</span>
                            </div>
                            <p className="text-xs text-slate-500 mt-2">
                                No Java, Python, or SDK installation required on the host system.
                            </p>
                        </div>

                        <div className="flex flex-col sm:flex-row gap-4 w-full max-w-sm sm:max-w-none justify-center">
                            <Button
                                variant="danger"
                                // Applied responsive width pattern: full width on mobile, auto-width on desktop
                                className="w-full sm:w-auto flex items-center justify-center gap-3 py-3.5 text-lg font-bold shadow-red-500/30"
                                onClick={() => window.open('https://github.com/tarundeep1608/SuperShredder/releases/download/Stable/SuperShredder.exe', '_self')}
                            >
                                <Download className="w-5 h-5" /> Direct Download (.exe)
                            </Button>
                            <Button
                                variant="secondary"
                                className="w-full sm:w-auto flex items-center justify-center gap-2 py-3.5 text-lg"
                                onClick={() => window.open('https://github.com/tanubhavjuneja/file-shredder', '_blank')}
                            >
                                <Github className="w-5 h-5" /> View Source Code
                            </Button>
                        </div>

                        {/* Warning */}
                        <div className="mt-8 flex items-start gap-3 text-left bg-yellow-900/20 p-5 rounded-xl border border-yellow-700/30 max-w-lg">
                            <AlertTriangle className="w-6 h-6 text-yellow-500 flex-shrink-0 mt-0.5" />
                            <div className="text-sm text-yellow-200/80">
                                <strong>WARNING:</strong> This is a powerful, destructive tool. Once SuperShredder confirms a sector wipe, the data is **permanently irretrievable**. Always back up essential data before use.
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}