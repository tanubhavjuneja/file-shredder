/**
 * @fileoverview Reusable Button Component
 * 
 * A flexible, styled button component that supports multiple visual variants.
 * Built with Tailwind CSS for consistent theming across the application.
 * 
 * @author Team PD Lovers
 * @version 1.0.0
 */

import React from 'react';

/**
 * Reusable Button Component
 * 
 * Renders a styled button with configurable variants for different use cases.
 * Supports all standard button HTML attributes via props spreading.
 * 
 * @param {Object} props - Component props
 * @param {React.ReactNode} props.children - Button content/label
 * @param {'primary'|'danger'|'secondary'|'ghost'} [props.variant='primary'] - Visual style variant
 * @param {string} [props.className=''] - Additional CSS classes to apply
 * @param {Object} props.rest - Any additional props passed to the button element
 * @returns {JSX.Element} A styled button element
 * 
 * @example
 * // Primary button (default)
 * <Button onClick={handleClick}>Click Me</Button>
 * 
 * @example
 * // Danger variant for destructive actions
 * <Button variant="danger">Delete</Button>
 * 
 * @example
 * // Secondary outline style
 * <Button variant="secondary">Cancel</Button>
 */
export default function Button({ children, variant = 'primary', className = '', ...props }) {
    // Base styles applied to all button variants
    const baseStyles = "px-6 py-3 rounded-md font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900";

    // Variant-specific style mappings
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