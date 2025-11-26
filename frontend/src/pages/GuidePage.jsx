import React, { useState } from 'react';
import { Terminal, Play, Cpu, Download, ChevronRight, Command, Shield, GitBranch, Box, Hammer } from 'lucide-react';
import SectionHeader from '../components/SectionHeader';

export default function GuidePage() {
    const [activeTab, setActiveTab] = useState('user'); // 'user' or 'dev'

    const userSteps = [
        {
            num: "01",
            title: "Launch Application",
            desc: "Download and run the portable `SuperShredder.exe`. No installation is required, but Administrator privileges are necessary to access physical drive partitions.",
            icon: <Play className="w-6 h-6 text-blue-400" />
        },
        {
            num: "02",
            title: "Select Target",
            desc: "Choose 'Windows' to detect local NTFS/FAT32 drives or 'Android' to bridge with connected devices via ADB. The tool automatically scans for available targets.",
            icon: <Cpu className="w-6 h-6 text-purple-400" />
        },
        {
            num: "03",
            title: "Configure Algorithm",
            desc: "Select your sanitization standard. 'DoD 5220.22-M' performs 3 passes (Zeros, Ones, Random) for classified data, while 'Zero Fill' offers speed for general use.",
            icon: <Shield className="w-6 h-6 text-yellow-400" />
        },
        {
            num: "04",
            title: "Execute & Verify",
            desc: "Click 'Shred'. The worker threads will lock the filesystem handles and begin overwriting. A final verification hash confirms the data is unrecoverable.",
            icon: <Terminal className="w-6 h-6 text-green-400" />
        }
    ];

    const devSteps = [
        {
            step: "1. Clone Repository",
            desc: "Get the latest source code from GitHub.",
            cmd: "git clone https://github.com/tarundeep1608/SuperShredder.git\ncd SuperShredder"
        },
        {
            step: "2. Run from Source",
            desc: "Execute the raw Python script. Requires Python 3.13+.",
            cmd: "pip install -r requirements.txt\npython main.py"
        },
        {
            step: "3. Build Binary",
            desc: "Compile into a standalone executable using the build script.",
            cmd: "python build.py\n# Output will be in /dist/SuperShredder.exe"
        }
    ];

    return (
        <section id="guide" className="relative min-h-screen flex flex-col justify-center py-24 bg-slate-950 overflow-hidden">

            {/* Background Grid */}
            <div className="absolute inset-0 z-0 opacity-20 pointer-events-none"
                 style={{
                     backgroundImage: 'linear-gradient(#1e293b 1px, transparent 1px), linear-gradient(to right, #1e293b 1px, transparent 1px)',
                     backgroundSize: '40px 40px'
                 }}
            ></div>

            <div className="container mx-auto px-6 relative z-10">
                <SectionHeader
                    title="Documentation"
                    subtitle="Operational guide and developer resources."
                    centered={true}
                />

                {/* Tab Switcher */}
                <div className="flex justify-center mb-12">
                    <div className="bg-slate-900/80 p-1.5 rounded-xl border border-slate-800 flex gap-2 backdrop-blur-md">
                        <button
                            onClick={() => setActiveTab('user')}
                            className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${activeTab === 'user' ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/20' : 'text-slate-400 hover:text-white hover:bg-slate-800'}`}
                        >
                            <Download className="w-4 h-4" /> User Manual
                        </button>
                        <button
                            onClick={() => setActiveTab('dev')}
                            className={`px-6 py-2.5 rounded-lg text-sm font-medium transition-all flex items-center gap-2 ${activeTab === 'dev' ? 'bg-purple-600 text-white shadow-lg shadow-purple-900/20' : 'text-slate-400 hover:text-white hover:bg-slate-800'}`}
                        >
                            <GitBranch className="w-4 h-4" /> Developer Guide
                        </button>
                    </div>
                </div>

                {/* Content Area */}
                <div className="max-w-5xl mx-auto">

                    {/* User Manual Grid View - Equal Heights */}
                    {activeTab === 'user' && (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {userSteps.map((step, idx) => (
                                <div key={idx} className="group h-full">
                                    <div className="h-full bg-slate-900/50 backdrop-blur-sm border border-slate-800 p-8 rounded-2xl hover:border-blue-500/30 transition-all hover:-translate-y-1 hover:shadow-xl hover:shadow-blue-900/10 flex flex-col relative overflow-hidden">

                                        {/* Background Number */}
                                        <div className="absolute -right-4 -top-4 text-9xl font-bold text-slate-800/30 select-none group-hover:text-blue-900/10 transition-colors">
                                            {step.num}
                                        </div>

                                        <div className="relative z-10 flex flex-col h-full">
                                            <div className="mb-6 p-3 bg-slate-950 rounded-xl border border-slate-800 w-fit group-hover:scale-110 transition-transform shadow-lg">
                                                {step.icon}
                                            </div>

                                            <h3 className="text-xl font-bold text-white mb-3 group-hover:text-blue-400 transition-colors">
                                                {step.title}
                                            </h3>

                                            <p className="text-slate-400 leading-relaxed text-sm flex-grow">
                                                {step.desc}
                                            </p>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Developer Build View */}
                    {activeTab === 'dev' && (
                        <div className="max-w-3xl mx-auto">
                            <div className="bg-black/50 backdrop-blur-md border border-slate-800 rounded-2xl overflow-hidden shadow-2xl">
                                <div className="bg-slate-900/80 px-4 py-3 border-b border-slate-800 flex items-center justify-between">
                                    <div className="flex items-center gap-2">
                                        <Terminal className="w-4 h-4 text-slate-400" />
                                        <span className="text-sm font-mono text-slate-300">developer_setup.sh</span>
                                    </div>
                                    <div className="flex gap-1.5">
                                        <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
                                        <div className="w-2.5 h-2.5 rounded-full bg-slate-700"></div>
                                    </div>
                                </div>

                                <div className="p-6 md:p-8 space-y-8">
                                    {devSteps.map((item, index) => (
                                        <div key={index} className="group">
                                            <div className="flex items-center gap-3 text-white mb-2">
                                                {index === 0 && <GitBranch className="w-5 h-5 text-orange-500" />}
                                                {index === 1 && <Play className="w-5 h-5 text-green-500" />}
                                                {index === 2 && <Hammer className="w-5 h-5 text-blue-500" />}
                                                <h4 className="font-bold text-lg">{item.step}</h4>
                                            </div>
                                            <p className="text-slate-400 text-sm mb-3 pl-8">{item.desc}</p>

                                            <div className="pl-8">
                                                <div className="bg-slate-950 rounded-lg border border-slate-800 p-4 font-mono text-sm text-blue-300 shadow-inner relative overflow-hidden">
                                                    <div className="absolute top-0 left-0 w-1 h-full bg-slate-800 group-hover:bg-blue-600 transition-colors"></div>
                                                    <pre className="whitespace-pre-wrap">{item.cmd}</pre>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            <div className="mt-6 text-center text-xs text-slate-500 font-mono">
                                Requires <span className="text-slate-400">Python 3.13+</span> and <span className="text-slate-400">Admin Privileges</span> for disk I/O.
                            </div>
                        </div>
                    )}

                </div>
            </div>
        </section>
    );
}