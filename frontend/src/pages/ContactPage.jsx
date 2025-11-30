/**
 * @fileoverview Contact Page Component
 * 
 * Provides a contact form for users to submit feedback, bug reports,
 * or feature requests. Integrates with the backend API for form submission.
 * 
 * @author Team PD Lovers
 * @version 1.0.0
 */

import React, { useState } from 'react';
import { Send, CheckCircle, AlertCircle, Mail, MessageSquare } from 'lucide-react';
import SectionHeader from '../components/SectionHeader';
import Button from '../components/Button';
import { api } from '../services/api';

/**
 * Contact Page Component
 * 
 * Renders a contact form with:
 * - Email input field
 * - Message textarea
 * - Submit button with loading state
 * - Success/error feedback messages
 * 
 * Form states:
 * - 'idle': Ready for input
 * - 'sending': Submission in progress
 * - 'sent': Successfully submitted
 * - 'error': Submission failed
 * 
 * @returns {JSX.Element} The contact section
 */
export default function ContactPage() {
    /** @type {['idle'|'sending'|'sent'|'error', Function]} Form submission status */
    const [status, setStatus] = useState('idle');
    
    /** @type {[{email: string, message: string}, Function]} Form field values */
    const [formData, setFormData] = useState({ email: '', message: '' });

    /**
     * Updates form data when input fields change.
     * 
     * @param {React.ChangeEvent<HTMLInputElement|HTMLTextAreaElement>} e - The change event
     */
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.id]: e.target.value });
    };

    /**
     * Handles form submission.
     * Sends data to the backend API and updates status accordingly.
     * 
     * @param {React.FormEvent<HTMLFormElement>} e - The form submit event
     */
    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('sending');

        try {
            await api.submitContactForm(formData);
            setStatus('sent');
            setFormData({ email: '', message: '' });
        } catch (error) {
            setStatus('error');
        }
    };

    return (
        <section id="contact" className="relative min-h-screen flex flex-col items-center justify-center py-24 bg-slate-950 overflow-hidden">

            {/* Background Grid - Consistent */}
            <div className="absolute inset-0 z-0 opacity-20 pointer-events-none"
                 style={{
                     backgroundImage: 'linear-gradient(#1e293b 1px, transparent 1px), linear-gradient(to right, #1e293b 1px, transparent 1px)',
                     backgroundSize: '40px 40px'
                 }}
            ></div>

            {/* Ambient Glows */}
            <div className="absolute top-1/4 right-0 w-[400px] h-[400px] bg-blue-600/10 rounded-full blur-[100px] -z-10 pointer-events-none"></div>

            <div className="container mx-auto px-6 relative z-10">
                <SectionHeader
                    title="Get In Touch"
                    subtitle="Found a security vulnerability, bug, or have a feature request?"
                    centered={true}
                />

                <div className="max-w-xl mx-auto mt-12 bg-slate-900/50 backdrop-blur-md border border-slate-700 rounded-3xl p-8 md:p-10 shadow-2xl shadow-black/50 ring-1 ring-white/5">

                    {/* Status Messages */}
                    {status === 'sent' ? (
                        <div className="bg-green-500/10 border border-green-500/30 rounded-xl p-8 text-center animate-fade-in">
                            <div className="flex justify-center mb-4">
                                <CheckCircle className="w-12 h-12 text-green-500" />
                            </div>
                            <h3 className="text-xl font-bold text-white mb-2">Message Received</h3>
                            <p className="text-slate-400">Thank you for your feedback. We will review your message shortly.</p>
                            <button onClick={() => setStatus('idle')} className="mt-6 text-green-400 hover:text-green-300 underline font-medium">
                                Send another message
                            </button>
                        </div>
                    ) : (
                        <form onSubmit={handleSubmit} className="space-y-6">

                            {/* Error Alert */}
                            {status === 'error' && (
                                <div className="p-4 bg-red-900/20 border border-red-500/50 rounded-xl flex items-center gap-3 text-red-200 animate-fade-in">
                                    <AlertCircle className="w-5 h-5 flex-shrink-0" />
                                    <span className="text-sm">Failed to send message. Please ensure your backend server is running.</span>
                                </div>
                            )}

                            {/* Email Input */}
                            <div>
                                <label htmlFor="email" className="block text-sm font-medium text-slate-400 mb-2 flex items-center gap-2">
                                    <Mail className="w-4 h-4 text-blue-500" /> Email Address
                                </label>
                                <input
                                    type="email"
                                    id="email"
                                    value={formData.email}
                                    onChange={handleChange}
                                    required
                                    className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                    placeholder="your-secure-email@example.com"
                                    disabled={status === 'sending'}
                                />
                            </div>

                            {/* Message Textarea */}
                            <div>
                                <label htmlFor="message" className="block text-sm font-medium text-slate-400 mb-2 flex items-center gap-2">
                                    <MessageSquare className="w-4 h-4 text-blue-500" /> Message
                                </label>
                                <textarea
                                    id="message"
                                    value={formData.message}
                                    onChange={handleChange}
                                    rows={5}
                                    required
                                    className="w-full px-4 py-3 bg-slate-900 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                                    placeholder="Describe the issue or suggestion in detail..."
                                    disabled={status === 'sending'}
                                />
                            </div>

                            {/* Submit Button */}
                            <Button
                                type="submit"
                                variant="primary"
                                className="w-full flex justify-center items-center gap-3 py-3.5 text-lg"
                                disabled={status === 'sending'}
                            >
                                {status === 'sending' ? (
                                    'Sending Securely...'
                                ) : (
                                    <>
                                        <Send className="w-5 h-5" /> Send Message
                                    </>
                                )}
                            </Button>
                        </form>
                    )}
                </div>
            </div>
        </section>
    );
}