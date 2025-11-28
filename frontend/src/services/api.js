/**
 * ==================================================================================
 * API LAYER
 * ==================================================================================
 * Connects to the Django Backend
 */

const API_BASE_URL = 'https://fileshredder.pythonanywhere.com/api/v1';

export const api = {
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

    getLatestVersion: () => {
        // We can leave this static for now, or create a backend endpoint for it later
        return "1.0.0";
    }
};