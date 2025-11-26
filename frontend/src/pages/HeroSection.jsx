import React from 'react';
import Button from '../components/Button';
import { Download, ShieldCheck, ChevronRight, ChevronDown, Terminal, Shield } from 'lucide-react';

export default function HeroSection() {
    const scrollTo = (id) => {
        document.getElementById(id)?.scrollIntoView({ behavior: 'smooth' });
    };

    return (
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">

            {/* Background Grid Pattern */}
            <div className="absolute inset-0 z-0 opacity-20"
                 style={{
                     backgroundImage: 'linear-gradient(#1e293b 1px, transparent 1px), linear-gradient(to right, #1e293b 1px, transparent 1px)',
                     backgroundSize: '40px 40px'
                 }}
            ></div>

            {/* Ambient Glows */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10 pointer-events-none">
                <div className="absolute top-[-10%] right-[-5%] w-[500px] h-[500px] bg-blue-600/20 rounded-full blur-[100px] animate-pulse"></div>
                <div className="absolute bottom-[-10%] left-[-10%] w-[600px] h-[600px] bg-red-600/10 rounded-full blur-[120px]"></div>
                <div className="absolute top-[20%] left-[20%] w-[300px] h-[300px] bg-purple-500/10 rounded-full blur-[80px]"></div>
            </div>

            <div className="container mx-auto px-6 text-center relative z-10">

                {/* Release Badge */}
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-slate-900/80 border border-slate-700 backdrop-blur-sm text-blue-400 text-sm font-medium mb-8 animate-fade-in hover:border-blue-500/50 transition-colors cursor-default">
                    <span className="relative flex h-2 w-2">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                    </span>
                    v1.0 Stable Release Available
                </div>

                {/* Main Headline */}
                <h1 className="text-5xl md:text-7xl lg:text-8xl font-extrabold text-white tracking-tight mb-8 leading-tight">
                    Permanent Data <br />
                    <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-red-500 drop-shadow-2xl">
                        Destruction
                    </span>
                </h1>

                {/* Subtitle */}
                <p className="text-lg md:text-xl text-slate-400 max-w-2xl mx-auto mb-10 leading-relaxed">
                    Military-grade file shredding for <span className="text-blue-400 font-semibold">Windows</span> and <span className="text-green-400 font-semibold">Android</span>.
                    Ensure your sensitive data is gone forever with DoD 5220.22-M algorithms.
                </p>

                {/* CTA Buttons */}
                <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
                    <Button
                        variant="primary"
                        className="w-full sm:w-auto flex items-center justify-center gap-2 group px-8 py-4 text-lg shadow-blue-500/20 shadow-lg"
                        onClick={() => scrollTo('download')}
                    >
                        <Download className="w-5 h-5 group-hover:-translate-y-1 transition-transform" />
                        Download Now
                        <span className="text-xs opacity-70 font-normal ml-1 bg-blue-700/50 px-2 py-0.5 rounded">Free</span>
                    </Button>

                    <Button
                        variant="secondary"
                        className="w-full sm:w-auto flex items-center justify-center gap-2 group px-8 py-4 text-lg backdrop-blur-sm bg-slate-900/50"
                        onClick={() => scrollTo('specs')}
                    >
                        <ShieldCheck className="w-5 h-5 text-green-400" />
                        Safety Audit
                        <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform opacity-50 group-hover:opacity-100" />
                    </Button>
                </div>

                {/* Feature Pills */}
                <div className="flex flex-wrap justify-center gap-6 text-sm text-slate-500 font-medium">
                    <div className="flex items-center gap-2">
                        <Terminal className="w-4 h-4 text-slate-400" /> Open Source
                    </div>
                    <div className="w-1 h-1 rounded-full bg-slate-700"></div>
                    <div className="flex items-center gap-2">
                        <Shield className="w-4 h-4 text-slate-400" /> Zero Dependencies
                    </div>
                    <div className="w-1 h-1 rounded-full bg-slate-700"></div>
                    <div className="flex items-center gap-2">
                        <span>Running on <span className="text-yellow-500">Python 3.13</span></span>
                    </div>
                </div>
            </div>

            {/* Scroll Indicator */}
            <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce cursor-pointer" onClick={() => scrollTo('preview')}>
                <ChevronDown className="w-8 h-8 text-slate-600 hover:text-white transition-colors" />
            </div>
        </section>
    );
}