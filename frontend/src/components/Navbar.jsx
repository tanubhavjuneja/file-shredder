import React, { useState, useEffect } from 'react';
import { Menu, X, Trash2, Github, Download, Terminal } from 'lucide-react';
import Button from './Button';

export default function Navbar() {
    const [isOpen, setIsOpen] = useState(false);
    const [scrolled, setScrolled] = useState(false);

    // Constant height navbar for fixed top offset
    const NAVBAR_HEIGHT_PX = 88;

    // Add scroll listener to change navbar appearance when scrolling down
    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    const navLinks = [
        { name: 'Live Demo', href: '#preview', icon: <Terminal className="w-4 h-4" /> },
        { name: 'Features', href: '#features' },
        { name: 'Tech Specs', href: '#specs' },
        { name: 'Guide', href: '#guide' },
        { name: 'Support', href: '#contact' },
    ];

    const handleScroll = (id) => {
        const element = document.getElementById(id.replace('#', ''));
        if (element) {
            // Offset for the fixed header
            const headerOffset = 80;
            const offsetPosition = element.getBoundingClientRect().top + window.scrollY - headerOffset;
            window.scrollTo({ top: offsetPosition, behavior: "smooth" });
            setIsOpen(false);
        }
    };

    // Determine the classes for the main <nav> element
    const navClasses = `fixed w-full z-50 transition-all duration-300 py-4 bg-slate-950 ${
        scrolled || isOpen
            ? 'border-b border-slate-800 shadow-lg shadow-black/50'
            : 'border-b border-transparent shadow-none'
    }`;

    return (
        <nav
            className={navClasses}
        >
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-14">

                    {/* Logo */}
                    <div
                        className="flex-shrink-0 flex items-center gap-3 cursor-pointer group"
                        onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
                    >
                        <div className="relative">
                            <div className="absolute inset-0 bg-red-500 opacity-20 group-hover:opacity-40 transition-opacity"></div>
                            <Trash2 className="h-7 w-7 text-red-500 relative z-10" />
                        </div>
                        <span className="font-bold text-xl tracking-wider text-white">
                            SUPER<span className="text-red-500">SHREDDER</span>
                        </span>
                    </div>

                    {/* Desktop Nav */}
                    <div className="hidden lg:block">
                        <div className="ml-10 flex items-center space-x-6">
                            {navLinks.map((link) => (
                                <button
                                    key={link.name}
                                    onClick={() => handleScroll(link.href)}
                                    className="flex items-center gap-2 text-slate-300 hover:text-white px-3 py-2 rounded-md text-sm font-medium transition-all hover:bg-slate-800/50"
                                >
                                    {link.icon && <span className="text-slate-500 group-hover:text-white transition-colors">{link.icon}</span>}
                                    {link.name}
                                </button>
                            ))}

                            <div className="h-6 w-px bg-slate-700 mx-2"></div>

                            <a
                                href="https://github.com/tarundeep1608/supershredder"
                                target="_blank"
                                rel="noreferrer"
                                className="text-slate-400 hover:text-white transition-colors"
                            >
                                <Github className="w-5 h-5" />
                            </a>

                            <Button
                                variant="danger"
                                className="py-2 px-5 text-sm flex items-center gap-2 shadow-red-500/20"
                                onClick={() => handleScroll('#download')}
                            >
                                <Download className="w-4 h-4" />
                                Download
                            </Button>
                        </div>
                    </div>

                    {/* Mobile menu button */}
                    <div className="lg:hidden flex items-center gap-4">
                        <Button
                            variant="danger"
                            className="py-1.5 px-3 text-xs md:hidden"
                            onClick={() => handleScroll('#download')}
                        >
                            Get App
                        </Button>
                        <button
                            onClick={() => setIsOpen(!isOpen)}
                            className="text-slate-300 hover:text-white p-2 rounded-md hover:bg-slate-800 transition-colors"
                        >
                            {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
                        </button>
                    </div>
                </div>
            </div>

            {/* Mobile Nav Menu (Uses solid bg-slate-950) */}
            <div
                className={`lg:hidden fixed inset-0 z-40 bg-slate-950 transition-transform duration-300 ease-in-out ${
                    isOpen ? 'translate-x-0' : 'translate-x-full'
                }`}
                style={{ top: `${NAVBAR_HEIGHT_PX}px` }}
            >
                <div className="px-4 pt-6 pb-8 space-y-2 border-t border-slate-800">
                    {navLinks.map((link) => (
                        <button
                            key={link.name}
                            onClick={() => handleScroll(link.href)}
                            className="text-slate-300 hover:text-white hover:bg-slate-800 block w-full text-left px-4 py-4 rounded-lg text-lg font-medium transition-all border border-transparent hover:border-slate-700"
                        >
                            <span className="flex items-center gap-3">
                                {link.icon} {link.name}
                            </span>
                        </button>
                    ))}

                    <div className="pt-4 border-t border-slate-800 space-y-2">
                        <a
                            href="https://github.com/tarundeep1608/supershredder"
                            target="_blank"
                            rel="noreferrer"
                            className="w-full justify-center flex items-center gap-3 text-slate-400 hover:text-white bg-slate-800/50 hover:bg-slate-800/80 px-4 py-4 rounded-md text-lg font-medium transition-colors"
                        >
                            <Github className="w-5 h-5" /> View Source on GitHub
                        </a>

                        <Button
                            variant="danger"
                            // FIX: Added 'gap-3' to ensure proper spacing between the icon and text.
                            className="w-full flex items-center justify-center gap-3 py-4 text-lg whitespace-nowrap"
                            onClick={() => handleScroll('#download')}
                        >
                            <Download className="w-5 h-5 flex-shrink-0" />
                            Download SuperShredder
                        </Button>
                    </div>
                </div>
            </div>
        </nav>
    );
}