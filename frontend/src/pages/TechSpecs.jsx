import React from 'react';
import { ShieldAlert, FileCode, Cpu, Layers, Terminal, Lock, AlertTriangle, Zap } from 'lucide-react';
import SectionHeader from '../components/SectionHeader';

export default function TechSpecs() {
    return (
        <section id="specs" className="relative min-h-screen flex flex-col justify-center py-24 bg-slate-950 overflow-hidden">

            {/* Background Grid - Consistent with Hero & Preview */}
            <div className="absolute inset-0 z-0 opacity-20 pointer-events-none"
                 style={{
                     backgroundImage: 'linear-gradient(#1e293b 1px, transparent 1px), linear-gradient(to right, #1e293b 1px, transparent 1px)',
                     backgroundSize: '40px 40px'
                 }}
            ></div>

            {/* Ambient Glows */}
            <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-red-600/5 rounded-full blur-[120px] -z-10 pointer-events-none"></div>
            <div className="absolute bottom-0 left-0 w-[600px] h-[600px] bg-blue-600/5 rounded-full blur-[120px] -z-10 pointer-events-none"></div>

            <div className="container mx-auto px-6 relative z-10">
                <SectionHeader
                    title="Technical Specifications"
                    subtitle="Under the hood of the Python 3.13 wiping engine."
                    centered={true}
                />

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 mt-16 max-w-6xl mx-auto">

                    {/* Left Column: Algorithms */}
                    <div className="space-y-8">
                        <div className="flex items-center gap-4 mb-2">
                            <div className="p-3 bg-red-500/10 rounded-xl border border-red-500/20">
                                <ShieldAlert className="w-8 h-8 text-red-500" />
                            </div>
                            <div>
                                <h3 className="text-2xl font-bold text-white">Destruction Algorithms</h3>
                                <p className="text-slate-400 text-sm">Standard-compliant data sanitization methods.</p>
                            </div>
                        </div>

                        {/* Algorithm Cards */}
                        <div className="group bg-slate-900/50 backdrop-blur-sm p-6 rounded-2xl border border-slate-800 hover:border-red-500/30 transition-all hover:bg-slate-800/80">
                            <div className="flex justify-between items-start mb-2">
                                <h4 className="text-lg font-bold text-blue-400">DoD 5220.22-M</h4>
                                <span className="px-2 py-1 bg-blue-900/30 text-blue-300 text-xs rounded border border-blue-800">3 Passes</span>
                            </div>
                            <p className="text-slate-400 text-sm leading-relaxed">
                                The industry standard. Executes three distinct overwrite passes:
                                <span className="text-slate-300 font-mono mx-1">0x00</span> →
                                <span className="text-slate-300 font-mono mx-1">0xFF</span> →
                                <span className="text-slate-300 font-mono mx-1">Random</span>.
                                Verifies writes to ensure magnetic unrecoverability.
                            </p>
                        </div>

                        <div className="group bg-slate-900/50 backdrop-blur-sm p-6 rounded-2xl border border-slate-800 hover:border-green-500/30 transition-all hover:bg-slate-800/80">
                            <div className="flex justify-between items-start mb-2">
                                <h4 className="text-lg font-bold text-green-400">Zero Fill (Quick)</h4>
                                <span className="px-2 py-1 bg-green-900/30 text-green-300 text-xs rounded border border-green-800">1 Pass</span>
                            </div>
                            <p className="text-slate-400 text-sm leading-relaxed">
                                A single high-speed pass of zeros. Ideal for clearing free space or preparing SSDs where excessive write cycles can degrade hardware lifespan.
                            </p>
                        </div>

                        <div className="group bg-slate-900/50 backdrop-blur-sm p-6 rounded-2xl border border-slate-800 hover:border-purple-500/30 transition-all hover:bg-slate-800/80">
                            <div className="flex justify-between items-start mb-2">
                                <h4 className="text-lg font-bold text-purple-400">Cryptographic Random</h4>
                                <span className="px-2 py-1 bg-purple-900/30 text-purple-300 text-xs rounded border border-purple-800">1 Pass</span>
                            </div>
                            <p className="text-slate-400 text-sm leading-relaxed">
                                Overwrites sectors with cryptographically secure pseudo-random data (CSPRNG), confusing pattern-based recovery tools and analysis.
                            </p>
                        </div>
                    </div>

                    {/* Right Column: Architecture */}
                    <div className="space-y-8">
                        <div className="flex items-center gap-4 mb-2">
                            <div className="p-3 bg-blue-500/10 rounded-xl border border-blue-500/20">
                                <Cpu className="w-8 h-8 text-blue-500" />
                            </div>
                            <div>
                                <h3 className="text-2xl font-bold text-white">System Architecture</h3>
                                <p className="text-slate-400 text-sm">Built for speed, portability, and safety.</p>
                            </div>
                        </div>

                        <div className="relative border-l-2 border-slate-800 pl-8 space-y-8 py-2">
                            {/* Timeline Item 1 */}
                            <div className="relative">
                                <div className="absolute -left-[41px] top-1 w-6 h-6 bg-slate-900 border-2 border-yellow-500 rounded-full flex items-center justify-center">
                                    <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
                                </div>
                                <h5 className="text-lg font-bold text-white flex items-center gap-2">
                                    <FileCode className="w-4 h-4 text-yellow-500" /> Python 3.13 Core
                                </h5>
                                <p className="text-slate-400 text-sm mt-1">
                                    Leverages the latest Python runtime features. IO-bound operations are offloaded to separate worker threads to keep the UI responsive during heavy disk writes.
                                </p>
                            </div>

                            {/* Timeline Item 2 */}
                            <div className="relative">
                                <div className="absolute -left-[41px] top-1 w-6 h-6 bg-slate-900 border-2 border-teal-500 rounded-full"></div>
                                <h5 className="text-lg font-bold text-white flex items-center gap-2">
                                    <Layers className="w-4 h-4 text-teal-500" /> Portable ADB Stack
                                </h5>
                                <p className="text-slate-400 text-sm mt-1">
                                    Bundles a standalone <code>adb.exe</code> and <code>AdbWinApi.dll</code>. This allows the app to interface with Android devices without requiring the user to install the 2GB+ Android SDK.
                                </p>
                            </div>

                            {/* Timeline Item 3 */}
                            <div className="relative">
                                <div className="absolute -left-[41px] top-1 w-6 h-6 bg-slate-900 border-2 border-pink-500 rounded-full"></div>
                                <h5 className="text-lg font-bold text-white flex items-center gap-2">
                                    <Terminal className="w-4 h-4 text-pink-500" /> Sector-Level Access
                                </h5>
                                <p className="text-slate-400 text-sm mt-1">
                                    Bypasses standard file deletion APIs. Writes directly to the physical sectors of the drive partition to ensure data is actually destroyed, not just unlinked.
                                </p>
                            </div>
                        </div>

                        {/* Safety Warning Card */}
                        <div className="mt-8 p-5 border border-yellow-500/20 bg-yellow-500/5 rounded-xl flex gap-4">
                            <AlertTriangle className="w-10 h-10 text-yellow-500 flex-shrink-0" />
                            <div>
                                <h6 className="text-yellow-500 font-bold mb-1">Fail-Safe Protocols</h6>
                                <p className="text-sm text-yellow-200/60 leading-relaxed">
                                    The engine includes a hard-coded blocklist preventing write operations to the critical System Partition (C:/Windows) to prevent accidental OS self-destruction.
                                </p>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </section>
    );
}