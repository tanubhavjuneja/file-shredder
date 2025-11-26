import React from 'react';
import { Trash2, Heart, Download, GitBranch, Terminal, Shield, Github } from 'lucide-react';

export default function Footer() {
    const navLinks = [
        { name: 'Features', href: '#features', icon: <Shield className="w-4 h-4 text-blue-500" /> },
        { name: 'Live Demo', href: '#preview', icon: <Terminal className="w-4 h-4 text-purple-500" /> },
        { name: 'Tech Specs', href: '#specs', icon: <GitBranch className="w-4 h-4 text-yellow-500" /> },
        { name: 'Download', href: '#download', icon: <Download className="w-4 h-4 text-red-500" /> },
    ];

    const handleScroll = (id) => {
        const element = document.getElementById(id.replace('#', ''));
        if (element) {
            window.scrollTo({ top: element.offsetTop - 80, behavior: 'smooth' });
        }
    };

    return (
        <footer className="bg-slate-950 border-t border-slate-800 pt-16 pb-10">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

                {/* Top Section: Logo & Quick Links */}
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-12 gap-8 mb-12 border-b border-slate-800 pb-10">

                    {/* Logo/Brand (Column 1) */}
                    <div className="col-span-2 lg:col-span-4 flex flex-col items-start">
                        <div
                            className="flex-shrink-0 flex items-center gap-2 cursor-pointer"
                            onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                        >
                            <Trash2 className="h-7 w-7 text-red-500" />
                            <span className="font-bold text-xl tracking-wider text-white">
                                SUPER<span className="text-red-500">SHREDDER</span>
                            </span>
                        </div>
                        <p className="text-slate-500 text-sm mt-3 max-w-xs">
                            Permanent data destruction for peace of mind. Trusted by security researchers.
                        </p>
                    </div>

                    {/* Navigation Links (Column 2 & 3) */}
                    <div className="col-span-2 md:col-span-1 lg:col-span-2">
                        <h4 className="text-sm font-semibold text-white mb-4 uppercase tracking-wider">Navigation</h4>
                        <ul className="space-y-3">
                            {navLinks.slice(0, 2).map(link => (
                                <li key={link.name}>
                                    <button
                                        onClick={() => handleScroll(link.href)}
                                        className="text-slate-400 hover:text-white transition-colors text-sm flex items-center gap-2"
                                    >
                                        {link.icon} {link.name}
                                    </button>
                                </li>
                            ))}
                        </ul>
                    </div>

                    <div className="col-span-2 md:col-span-1 lg:col-span-2">
                        <h4 className="text-sm font-semibold text-white mb-4 uppercase tracking-wider">Resources</h4>
                        <ul className="space-y-3">
                            {navLinks.slice(2).map(link => (
                                <li key={link.name}>
                                    <button
                                        onClick={() => handleScroll(link.href)}
                                        className="text-slate-400 hover:text-white transition-colors text-sm flex items-center gap-2"
                                    >
                                        {link.icon} {link.name}
                                    </button>
                                </li>
                            ))}
                            <li>
                                <a href="https://github.com/tarundeep1608/supershredder" target="_blank" rel="noreferrer" className="text-slate-400 hover:text-white transition-colors text-sm flex items-center gap-2">
                                    <Github className="w-4 h-4 text-slate-500" /> GitHub Repo
                                </a>
                            </li>
                        </ul>
                    </div>

                    {/* Spacer / Contact (Column 4 - optional, but useful) */}
                    <div className="col-span-2 md:col-span-2 lg:col-span-4">
                        <h4 className="text-sm font-semibold text-white mb-4 uppercase tracking-wider">Disclaimer Summary</h4>
                        <p className="text-sm text-red-400 border border-red-900/50 bg-red-900/20 p-3 rounded-lg leading-relaxed">
                            <strong>Use with Caution:</strong> This tool is designed for permanent data loss. The developers are not responsible for any accidental or malicious misuse.
                        </p>
                    </div>

                </div>

                {/* Bottom Section: Copyright and Credits */}
                <div className="flex flex-col md:flex-row justify-between items-center text-xs text-slate-600 pt-4">

                    <p className="order-2 md:order-1 mt-4 md:mt-0">
                        &copy; {new Date().getFullYear()} Team PD Lovers. All Rights Reserved.
                    </p>

                    <div className="flex items-center order-1 md:order-2 gap-4">
                        <span className="text-slate-500">Version 1.0.0</span>
                        <div className="flex items-center gap-1 text-slate-500">
                            Built with <Heart className="w-3 h-3 text-red-500 fill-current" /> by Tarundeep Singh
                        </div>
                    </div>
                </div>
            </div>
        </footer>
    );
}