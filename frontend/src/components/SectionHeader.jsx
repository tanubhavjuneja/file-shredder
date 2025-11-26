import React from 'react';

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