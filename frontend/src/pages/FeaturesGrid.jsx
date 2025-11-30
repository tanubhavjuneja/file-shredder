/**
 * @fileoverview Features Grid Component
 * 
 * Displays the key features of SuperShredder in an attractive grid layout.
 * Each feature card highlights a specific capability with icon and description.
 * 
 * @author Team PD Lovers
 * @version 1.0.0
 */

import React from 'react';
import { Shield, Zap, Lock, RefreshCw, Smartphone, HardDrive } from 'lucide-react';
import SectionHeader from '../components/SectionHeader';

/**
 * Features Grid Component
 * 
 * Renders a responsive grid of feature cards showcasing:
 * - Military-grade standards (DoD 5220.22-M)
 * - Android ADB integration
 * - Native Windows engine
 * - Irreversible destruction
 * - Zero-config discovery
 * - Portable operation
 * 
 * @returns {JSX.Element} The features grid section
 */
export default function FeaturesGrid() {
    /**
     * Feature definitions for the grid.
     * Each feature has an icon, title, and description.
     */
    const features = [
        {
            icon: <Shield className="w-8 h-8 text-blue-500" />,
            title: "Military Grade Standards",
            description: "Implements the US DoD 5220.22-M sanitization protocol. Data is overwritten in three passes, making magnetic recovery statistically impossible."
        },
        {
            icon: <Smartphone className="w-8 h-8 text-green-500" />,
            title: "Android ADB Bridge",
            description: "Connect physically or wirelessly to Android devices. Directly wipes external storage partitions (/sdcard) without rooting."
        },
        {
            icon: <HardDrive className="w-8 h-8 text-purple-500" />,
            title: "Native Windows Engine",
            description: "Deep integration with NTFS and FAT32 file systems allows for sector-level access and locking prevention during deletion."
        },
        {
            icon: <Lock className="w-8 h-8 text-red-500" />,
            title: "Irreversible Destruction",
            description: "Files are not recycled. They are shredded, overwritten with entropy, and unlinked. Even electron microscopy cannot recover them."
        },
        {
            icon: <RefreshCw className="w-8 h-8 text-yellow-500" />,
            title: "Zero-Config Discovery",
            description: "Automatically detects connected USB drives, mounted partitions, and ADB-enabled mobile devices in real-time."
        },
        {
            icon: <Zap className="w-8 h-8 text-orange-500" />,
            title: "Portable & Lightweight",
            description: "No installation required. Runs as a standalone executable with zero external dependencies (bundled Python runtime)."
        }
    ];

    return (
        <section id="features" className="relative min-h-screen flex flex-col justify-center py-24 bg-slate-950 overflow-hidden">

            {/* Background Grid */}
            <div className="absolute inset-0 z-0 opacity-20 pointer-events-none"
                 style={{
                     backgroundImage: 'linear-gradient(#1e293b 1px, transparent 1px), linear-gradient(to right, #1e293b 1px, transparent 1px)',
                     backgroundSize: '40px 40px'
                 }}
            ></div>

            {/* Ambient Glows */}
            <div className="absolute top-1/4 left-0 w-[500px] h-[500px] bg-blue-600/10 rounded-full blur-[120px] -z-10 pointer-events-none"></div>
            <div className="absolute bottom-0 right-0 w-[600px] h-[600px] bg-purple-600/10 rounded-full blur-[120px] -z-10 pointer-events-none"></div>

            <div className="container mx-auto px-6 relative z-10">
                <SectionHeader
                    title="Why Choose SuperShredder?"
                    subtitle="Engineered for privacy enthusiasts, security researchers, and paranoia."
                    centered={true}
                />

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mt-12">
                    {features.map((feature, index) => (
                        <div
                            key={index}
                            className="group relative bg-slate-900/50 backdrop-blur-sm border border-slate-800 rounded-2xl p-8 hover:border-slate-600 hover:bg-slate-800/50 transition-all duration-300 hover:-translate-y-1 hover:shadow-2xl hover:shadow-black/50"
                        >
                            {/* Hover Glow Effect */}
                            <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity rounded-2xl pointer-events-none"></div>

                            <div className="relative z-10">
                                <div className="mb-6 inline-flex items-center justify-center w-16 h-16 rounded-xl bg-slate-950 border border-slate-800 shadow-lg group-hover:scale-110 transition-transform duration-300">
                                    {feature.icon}
                                </div>

                                <h3 className="text-xl font-bold text-white mb-3 group-hover:text-blue-400 transition-colors">
                                    {feature.title}
                                </h3>

                                <p className="text-slate-400 leading-relaxed text-sm">
                                    {feature.description}
                                </p>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}