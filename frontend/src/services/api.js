/**
 * @fileoverview API Service Layer
 * 
 * Provides a centralized interface for all backend API communications.
 * Currently connects to the Django backend hosted on PythonAnywhere.
 * 
 * @author Team PD Lovers
 * @version 1.0.0
 */

/**
 * Base URL for all API endpoints.
 * Points to the production Django backend.
 */
const API_BASE_URL = 'https://fileshredder.pythonanywhere.com/api/v1';

/**
 * API service object containing all available API methods.
 * 
 * @namespace
 */
export const api = {
    /**
     * Submits the contact form data to the backend.
     * 
     * @async
     * @param {Object} data - The form data to submit
     * @param {string} data.email - The user's email address
     * @param {string} data.message - The user's message
     * @returns {Promise<Object>} The JSON response from the server
     * @throws {Error} If the request fails or returns a non-OK status
     * 
     * @example
     * try {
     *   const response = await api.submitContactForm({
     *     email: 'user@example.com',
     *     message: 'Great app!'
     *   });
     *   console.log('Success:', response);
     * } catch (error) {
     *   console.error('Failed:', error);
     * }
     */
    submitContactForm: async (data) => {
        try {
            const response = await fetch(`${API_BASE_URL}/contact/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("API Error:", error);
            throw error;
        }
    },

    /**
     * Returns the latest application version.
     * Currently returns a static value; can be updated to fetch
     * from a backend endpoint in the future.
     * 
     * @returns {string} The current version string
     */
    getLatestVersion: () => {
        return "1.0.0";
    }
};