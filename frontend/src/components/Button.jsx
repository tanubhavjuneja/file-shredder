import React from 'react';

export default function Button({ children, variant = 'primary', className = '', ...props }) {
    const baseStyles = "px-6 py-3 rounded-md font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900";

    const variants = {
        primary: "bg-blue-600 hover:bg-blue-700 text-white focus:ring-blue-500 shadow-lg shadow-blue-900/20",
        danger: "bg-red-600 hover:bg-red-700 text-white focus:ring-red-500 shadow-lg shadow-red-900/20",
        secondary: "bg-transparent border border-slate-600 text-slate-300 hover:bg-slate-800 hover:text-white focus:ring-slate-500",
        ghost: "bg-transparent text-slate-400 hover:text-white hover:bg-slate-800/50"
    };

    return (
        <button
            className={`${baseStyles} ${variants[variant]} ${className}`}
            {...props}
        >
            {children}
        </button>
    );
}