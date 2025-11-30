/**
 * @fileoverview Interactive App Preview Component
 * 
 * This component provides an interactive simulation of the SuperShredder
 * application directly in the browser. It demonstrates both Windows and
 * Android wiping functionality with animated terminal output.
 * 
 * Features:
 * - Platform switching (Windows/Android)
 * - Simulated DoD 5220.22-M and Zero Fill algorithms
 * - ADB device connection simulation
 * - Real-time progress and log output
 * 
 * @author Team PD Lovers
 * @version 1.0.0
 */

import React, { useState, useEffect, useRef } from 'react';
import {
    Monitor,
    Smartphone,
    HardDrive,
    CheckCircle2,
    Shield,
    RefreshCw
} from 'lucide-react';
import Button from './Button';

/**
 * Interactive App Preview Component
 * 
 * Renders a simulated desktop application interface that demonstrates
 * the file shredding capabilities for both Windows and Android platforms.
 * 
 * @returns {JSX.Element} The interactive preview section
 */
export default function AppPreview() {
    // ==========================================
    // STATE MANAGEMENT
    // ==========================================
    
    /** @type {['windows'|'android', Function]} Currently active platform tab */
    const [activeTab, setActiveTab] = useState('windows');

    // ----- Windows-specific State -----
    /** @type {['DOD'|'ZERO', Function]} Selected wiping algorithm */
    const [winAlgorithm, setWinAlgorithm] = useState('DOD');
    /** @type {[string, Function]} Target drive letter (unused in simulation but kept for future) */
    const [winDrive, setWinDrive] = useState('C');

    // ----- Android-specific State -----
    /** @type {['SEARCHING'|'FOUND'|'CONNECTED', Function]} ADB connection status */
    const [adbStatus, setAdbStatus] = useState('ZB');
    /** @type {[string|null, Function]} Currently selected Android device ID */
    const [selectedDevice, setSelectedDevice] = useState(null);

    // ----- Shared Wiping State -----
    /** @type {[number, Function]} Current progress percentage (0-100) */
    const [progress, setProgress] = useState(0);
    /** @type {[boolean, Function]} Whether a wipe operation is in progress */
    const [isWiping, setIsWiping] = useState(false);
    /** @type {[string, Function]} Current status text for display */
    const [statusText, setStatusText] = useState('IDLE');
    /** @type {React.RefObject<HTMLDivElement>} Reference for auto-scrolling terminal */
    const scrollRef = useRef(null);

    /** @type {[string[], Function]} Array of terminal log messages */
    const [logs, setLogs] = useState([
        "> SuperShredder Core [Python 3.13] initialized",
        "> Loading Portable ADB Stack... OK",
        "> Ready."
    ]);

    // ==========================================
    // SIDE EFFECTS
    // ==========================================

    /**
     * Auto-scroll Effect
     * Automatically scrolls the terminal log container to the bottom
     * whenever new log entries are added.
     */
    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [logs]);

    /**
     * Tab Switch Effect
     * Resets the simulation state when switching between Windows and Android tabs.
     * For Android, initiates a simulated ADB device discovery sequence.
     */
    useEffect(() => {
        setIsWiping(false);
        setProgress(0);
        setStatusText('IDLE');
        if (activeTab === 'android') {
            setAdbStatus('SEARCHING');
            setSelectedDevice(null);
            addLog("Initializing ADB Bridge...");
            setTimeout(() => {
                setAdbStatus('FOUND');
                addLog("Found 1 device(s).");
            }, 1500);
        } else {
            addLog("Switched to Windows Native Mode.");
        }
    }, [activeTab]);

    // ==========================================
    // HELPER FUNCTIONS
    // ==========================================

    /**
     * Appends a message to the terminal log.
     * Keeps only the last 16 entries to prevent memory bloat.
     * 
     * @param {string} msg - The message to add to the log
     */
    const addLog = (msg) => {
        setLogs(prev => [...prev.slice(-15), `> ${msg}`]);
    };

    /**
     * Handles device selection in Android mode.
     * Updates the connection status and logs the connection details.
     * 
     * @param {string} device - The device identifier to connect to
     */
    const handleDeviceSelect = (device) => {
        setSelectedDevice(device);
        setAdbStatus('CONNECTED');
        addLog(`Connected to ${device}`);
        addLog("Status: ONLINE | USB Debugging: ENABLED");
    };

    // ==========================================
    // SIMULATION LOGIC
    // ==========================================

    /**
     * Initiates the wipe simulation based on the active platform.
     * Guards against multiple concurrent wipe operations.
     */
    const runSimulation = () => {
        if (isWiping) return;
        setIsWiping(true);
        setStatusText('WIPING');
        setProgress(0);

        if (activeTab === 'windows') {
            runWindowsWipe();
        } else {
            runAndroidWipe();
        }
    };

    /**
     * Simulates the Windows drive wiping process.
     * Implements a multi-pass algorithm simulation with sector-level logging.
     * DoD algorithm runs 3 passes; Zero Fill runs 1 pass.
     */
    const runWindowsWipe = () => {
        const passes = winAlgorithm === 'DOD' ? 3 : 1;
        addLog(`Target: ${winDrive}:/Users/Admin/Secrets`);
        addLog(`Algorithm: ${winAlgorithm === 'DOD' ? 'DoD 5220.22-M' : 'Zero Fill'}`);

        let currentProgress = 0;
        let pass = 1;

        const interval = setInterval(() => {
            currentProgress += (winAlgorithm === 'DOD' ? 0.8 : 2.5); // DoD is slower

            // Random Sector Logic
            if (Math.random() > 0.7) {
                const sector = Math.floor(Math.random() * 9999999).toString(16).toUpperCase();
                addLog(`[Pass ${pass}/${passes}] Overwriting sector 0x${sector}`);
            }

            // Pass transitions for DoD
            if (winAlgorithm === 'DOD') {
                if (currentProgress >= 33 && pass === 1) { pass = 2; addLog("Pass 1 Complete. Starting Pass 2..."); }
                if (currentProgress >= 66 && pass === 2) { pass = 3; addLog("Pass 2 Complete. Starting Pass 3..."); }
            }

            if (currentProgress >= 100) {
                completeWipe(interval, "Drive Sanitization Complete.");
            }
            setProgress(currentProgress);
        }, 100);
    };

    /**
     * Simulates the Android ADB-based wiping process.
     * Demonstrates the stages: binary push, shell execution, and data wipe.
     */
    const runAndroidWipe = () => {
        addLog(`Target: /sdcard/ (External Storage)`);
        addLog(`Sending 'wipetool' binary to ${selectedDevice}...`);

        let currentProgress = 0;
        let stage = 'PUSH'; // PUSH -> SHELL -> WIPE

        const interval = setInterval(() => {
            currentProgress += 1.5;

            // Simulation Stages
            if (currentProgress > 10 && stage === 'PUSH') {
                stage = 'SHELL';
                addLog("adb shell chmod +x /data/local/tmp/wipetool");
            }
            if (currentProgress > 25 && stage === 'SHELL') {
                stage = 'WIPE';
                addLog("adb shell ./wipetool --zero /sdcard");
            }
            if (stage === 'WIPE' && Math.random() > 0.8) {
                addLog(`Writing zeros... ${Math.floor(currentProgress)}%`);
            }

            if (currentProgress >= 100) {
                completeWipe(interval, "ADB Wipe Complete. Device Clean.");
            }
            setProgress(currentProgress);
        }, 100);
    };

    /**
     * Completes the wipe simulation and updates the UI.
     * Clears the interval timer and generates a verification hash.
     * 
     * @param {number} interval - The interval ID to clear
     * @param {string} msg - The completion message to display
     */
    const completeWipe = (interval, msg) => {
        clearInterval(interval);
        setIsWiping(false);
        setProgress(100);
        setStatusText('CLEAN');
        addLog(msg);
        addLog("Verification Hash: " + Math.random().toString(36).substring(7).toUpperCase());
    };

    // ==========================================
    // COMPONENT RENDER
    // ==========================================
    return (
        <section id="preview" className="relative min-h-screen flex flex-col items-center justify-center py-20 bg-slate-950 overflow-hidden">

            {/* Background Grid */}
            <div className="absolute inset-0 z-0 opacity-20 pointer-events-none"
                 style={{
                     backgroundImage: 'linear-gradient(#1e293b 1px, transparent 1px), linear-gradient(to right, #1e293b 1px, transparent 1px)',
                     backgroundSize: '40px 40px'
                 }}
            ></div>

            <div className="container mx-auto px-4 relative z-10">
                <div className="text-center mb-12">
                    <h2 className="text-3xl md:text-5xl font-bold text-white mb-4 tracking-tight">Interactive Preview</h2>
                    <p className="text-slate-400 max-w-xl mx-auto text-lg">
                        Test the <span className="text-yellow-400">DoD 5220.22-M</span> engine directly in your browser.
                    </p>
                </div>

                {/* Main Window */}
                <div className="max-w-5xl mx-auto bg-slate-900 rounded-xl border border-slate-700 shadow-2xl shadow-black/80 flex flex-col overflow-hidden ring-1 ring-white/10">

                    {/* Window Bar */}
                    <div className="bg-slate-800 px-4 py-3 flex items-center justify-between border-b border-slate-700">
                        <div className="flex items-center gap-3">
                            <div className="flex gap-2">
                                <div className="w-3 h-3 rounded-full bg-red-500/80"></div>
                                <div className="w-3 h-3 rounded-full bg-yellow-500/80"></div>
                                <div className="w-3 h-3 rounded-full bg-green-500/80"></div>
                            </div>
                            <div className="h-4 w-px bg-slate-600 mx-2"></div>
                            <div className="flex items-center gap-2 text-slate-300 text-xs font-bold tracking-wide">
                                <Shield className="w-3 h-3" />
                                <span>SuperShredder v1.0.0</span>
                            </div>
                        </div>
                        <div className="text-xs font-mono text-slate-500">
                            {activeTab === 'windows' ? 'WIN_NTFS' : 'ADB_BRIDGE'}
                        </div>
                    </div>

                    <div className="flex flex-col md:flex-row min-h-[500px]">

                        {/* Sidebar */}
                        <div className="w-full md:w-64 bg-slate-900 border-r border-slate-700 flex flex-col p-4">
                            <div className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-3">Platform</div>
                            <button
                                onClick={() => !isWiping && setActiveTab('windows')}
                                className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all mb-2 ${activeTab === 'windows' ? 'bg-blue-600/10 text-blue-400 border border-blue-600/20' : 'text-slate-400 hover:text-white hover:bg-slate-800'}`}
                            >
                                <Monitor className="w-5 h-5" /> Windows
                            </button>
                            <button
                                onClick={() => !isWiping && setActiveTab('android')}
                                className={`flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-all ${activeTab === 'android' ? 'bg-green-600/10 text-green-400 border border-green-600/20' : 'text-slate-400 hover:text-white hover:bg-slate-800'}`}
                            >
                                <Smartphone className="w-5 h-5" /> Android
                            </button>

                            <div className="mt-auto pt-6 border-t border-slate-800">
                                <div className="text-xs font-mono text-slate-600 mb-2">THREAD_WORKERS</div>
                                <div className="flex gap-1">
                                    {[1,2,3,4].map(i => <div key={i} className={`h-8 flex-1 rounded ${isWiping ? 'bg-green-500 animate-pulse' : 'bg-slate-800'}`}></div>)}
                                </div>
                            </div>
                        </div>

                        {/* Main Content Area */}
                        <div className="flex-1 bg-slate-950 p-6 md:p-8 flex flex-col">

                            <div className="h-40 mb-6 w-full">
                                {activeTab === 'windows' && (
                                    <div className="grid grid-cols-2 gap-4 h-full">
                                        <div className="space-y-2">
                                            <label className="text-xs text-slate-500 font-mono">TARGET DRIVE</label>
                                            <div className="p-3 bg-slate-900 border border-slate-800 rounded text-sm text-white flex items-center justify-between h-12">
                                                <span className="flex items-center gap-2"><HardDrive className="w-4 h-4 text-slate-400"/> Local Disk (C:)</span>
                                                <span className="text-xs text-slate-500">512GB</span>
                                            </div>
                                        </div>
                                        <div className="space-y-2">
                                            <label className="text-xs text-slate-500 font-mono">ALGORITHM</label>
                                            <div className="flex gap-2 h-12">
                                                <button
                                                    onClick={() => !isWiping && setWinAlgorithm('DOD')}
                                                    className={`flex-1 rounded text-sm font-medium border transition-all ${winAlgorithm === 'DOD' ? 'bg-yellow-500/10 border-yellow-500/50 text-yellow-500' : 'bg-slate-900 border-slate-800 text-slate-400'}`}
                                                >
                                                    DoD 3-Pass
                                                </button>
                                                <button
                                                    onClick={() => !isWiping && setWinAlgorithm('ZERO')}
                                                    className={`flex-1 rounded text-sm font-medium border transition-all ${winAlgorithm === 'ZERO' ? 'bg-blue-500/10 border-blue-500/50 text-blue-500' : 'bg-slate-900 border-slate-800 text-slate-400'}`}
                                                >
                                                    Zero Fill
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                )}

                                {activeTab === 'android' && (
                                    <div className="flex flex-col h-full">
                                        <div className="flex items-center justify-between mb-2">
                                            <label className="text-xs text-slate-500 font-mono">CONNECTED DEVICES</label>
                                            <div className="flex items-center gap-1 text-xs text-slate-500">
                                                <div className={`w-2 h-2 rounded-full ${adbStatus === 'SEARCHING' ? 'bg-yellow-500 animate-pulse' : 'bg-green-500'}`}></div>
                                                {adbStatus}
                                            </div>
                                        </div>

                                        <div className="bg-slate-900 border border-slate-800 rounded-lg overflow-hidden flex-1">
                                            {adbStatus === 'SEARCHING' && (
                                                <div className="flex flex-col items-center justify-center h-full text-slate-500 gap-2">
                                                    <RefreshCw className="w-5 h-5 animate-spin" />
                                                    <span className="text-sm">Scanning for ADB devices...</span>
                                                </div>
                                            )}
                                            {adbStatus !== 'SEARCHING' && (
                                                <div
                                                    onClick={() => !isWiping && handleDeviceSelect('Pixel_7_Pro_API33')}
                                                    className={`p-3 flex items-center justify-between cursor-pointer h-full transition-colors ${selectedDevice ? 'bg-green-900/10 border-l-2 border-green-500' : 'hover:bg-slate-800'}`}
                                                >
                                                    <div className="flex items-center gap-3">
                                                        <Smartphone className="w-5 h-5 text-slate-400" />
                                                        <div>
                                                            <div className="text-sm text-white font-medium">Google Pixel 7 Pro</div>
                                                            <div className="text-xs text-slate-500 font-mono">ID: 8A2X1004 • USB 3.0</div>
                                                        </div>
                                                    </div>
                                                    {selectedDevice ? <CheckCircle2 className="w-5 h-5 text-green-500" /> : <div className="px-2 py-1 bg-slate-800 text-xs rounded text-slate-400">Select</div>}
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                )}
                            </div>

                            {/* Fixed Height Terminal */}
                            <div className="h-64 shrink-0 bg-black rounded-lg border border-slate-800 p-4 font-mono text-xs overflow-hidden flex flex-col relative mb-4">
                                <div ref={scrollRef} className="flex-1 overflow-y-auto space-y-1 custom-scrollbar">
                                    {logs.map((log, i) => (
                                        <div key={i} className={
                                            log.includes('adb') ? 'text-blue-400' :
                                                log.includes('Complete') ? 'text-green-400' :
                                                    'text-slate-400'
                                        }>
                                            {log}
                                        </div>
                                    ))}
                                    {isWiping && <div className="text-green-500 animate-pulse">_</div>}
                                </div>
                            </div>

                            <Button
                                onClick={runSimulation}
                                disabled={(activeTab === 'android' && !selectedDevice) || isWiping}
                                className={`w-full py-4 rounded font-bold tracking-widest ${
                                    (activeTab === 'android' && !selectedDevice) ? 'bg-slate-800 text-slate-600 cursor-not-allowed' :
                                        isWiping ? 'bg-slate-800 text-slate-500' : 'bg-red-600 text-white hover:bg-red-700'
                                }`}
                            >
                                {activeTab === 'android' && !selectedDevice ? 'SELECT A DEVICE FIRST' : isWiping ? 'SANITIZATION IN PROGRESS...' : 'START SHREDDING SEQUENCE'}
                            </Button>

                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}