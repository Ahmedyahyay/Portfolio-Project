/**
 * API Utility Functions
 * Handles all communication with the Flask backend
 */

class ApiClient {
    constructor() {
        this.baseURL = 'http://localhost:5000';
        this.currentUser = null;
        
        // Load user from localStorage if available
        this.loadUserFromStorage();
    }

    /**
     * Make HTTP request to backend API with CORS support
     * @param {string} endpoint - API endpoint path
     * @param {Object} options - Fetch options
     * @returns {Promise<Object>} Response data
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const config = {
            mode: 'cors',
            credentials: 'omit',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                ...options.headers
            },
            ...options
        };
        
        try {
            const response = await fetch(url, config);
            
            // Check if response is ok before parsing JSON
            if (!response.ok) {
                let errorData;
                try {
                    errorData = await response.json();
                } catch {
                    errorData = { error: `HTTP error! status: ${response.status}` };
                }
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
        } catch (error) {
            // Enhanced error logging for debugging
            console.error('API Request failed:', {
                url,
                method: config.method || 'GET',
                error: error.message,
                stack: error.stack
            });
            
            // Check for CORS-specific errors
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                throw new Error('Network error: Unable to connect to server. Please check if the backend is running on port 5000.');
            }
            
            throw error;
        }
    }    /**
     * Register a new user
     * @param {Object} userData - User registration data
     * @returns {Promise<Object>} Registration response
     */
    async register(userData) {
        try {
            const response = await this.request('/api/register', {
                method: 'POST',
                body: userData
            });
            
            // Auto-login after successful registration
            if (response.message) {
                const loginData = {
                    email: userData.email,
                    password: userData.password
                };
                return await this.login(loginData);
            }
            
            return response;
        } catch (error) {
            throw new Error(error.message || 'Registration failed');
        }
    }

    /**
     * Login user
     * @param {Object} credentials - Login credentials
     * @returns {Promise<Object>} Login response
     */
    async login(credentials) {
        try {
            const response = await this.request('/api/login', {
                method: 'POST',
                body: credentials
            });
            
            if (response.user_id) {
                // Store user session
                this.currentUser = {
                    id: response.user_id,
                    email: credentials.email
                };
                
                this.saveUserToStorage();
                
                return response;
            }
            
            throw new Error('Invalid login response');
        } catch (error) {
            throw new Error(error.message || 'Login failed');
        }
    }

    /**
     * Logout current user
     */
    logout() {
        this.currentUser = null;
        this.clearUserFromStorage();
    }

    /**
     * Calculate BMI
     * @param {number} height - Height in cm
     * @param {number} weight - Weight in kg
     * @returns {Promise<Object>} BMI calculation result
     */
    async calculateBMI(height, weight) {
        try {
            return await this.request('/api/bmi', {
                method: 'POST',
                body: { height, weight }
            });
        } catch (error) {
            throw new Error(error.message || 'BMI calculation failed');
        }
    }

    /**
     * Send password reset request
     * @param {string} email - User email
     * @returns {Promise<Object>} Reset response
     */
    async forgotPassword(email) {
        try {
            return await this.request('/api/forgot-password', {
                method: 'POST',
                body: { email }
            });
        } catch (error) {
            throw new Error(error.message || 'Password reset request failed');
        }
    }

    /**
     * Check if user is authenticated
     * @returns {boolean} Authentication status
     */
    isAuthenticated() {
        return this.currentUser !== null;
    }

    /**
     * Get current user data
     * @returns {Object|null} Current user data
     */
    getCurrentUser() {
        return this.currentUser;
    }

    /**
     * Save user data to localStorage
     */
    saveUserToStorage() {
        if (this.currentUser) {
            localStorage.setItem('nutrition_user', JSON.stringify(this.currentUser));
        }
    }

    /**
     * Load user data from localStorage
     */
    loadUserFromStorage() {
        try {
            const userData = localStorage.getItem('nutrition_user');
            if (userData) {
                this.currentUser = JSON.parse(userData);
            }
        } catch (error) {
            console.error('Failed to load user from storage:', error);
            this.clearUserFromStorage();
        }
    }

    /**
     * Clear user data from localStorage
     */
    clearUserFromStorage() {
        localStorage.removeItem('nutrition_user');
    }

    /**
     * Simulate meal history data (since /api/meal-history endpoint isn't implemented yet)
     * @returns {Array} Mock meal history data
     */
    async getMealHistory() {
        // This would normally be an API call, but for now we'll return mock data
        return new Promise(resolve => {
            setTimeout(() => {
                resolve([
                    {
                        id: 1,
                        meal: {
                            name: "Grilled Chicken Salad",
                            type: "lunch",
                            calories: 350,
                            ingredients: "chicken breast, mixed greens, tomatoes, cucumber"
                        },
                        date: new Date(Date.now() - 86400000).toISOString() // Yesterday
                    },
                    {
                        id: 2,
                        meal: {
                            name: "Oatmeal with Berries",
                            type: "breakfast",
                            calories: 280,
                            ingredients: "oats, blueberries, strawberries, almond milk"
                        },
                        date: new Date(Date.now() - 86400000).toISOString() // Yesterday
                    },
                    {
                        id: 3,
                        meal: {
                            name: "Baked Salmon with Quinoa",
                            type: "dinner",
                            calories: 420,
                            ingredients: "salmon fillet, quinoa, broccoli, lemon"
                        },
                        date: new Date(Date.now() - 172800000).toISOString() // 2 days ago
                    }
                ]);
            }, 500);
        });
    }

    /**
     * Simulate meal recommendations (since endpoint isn't implemented yet)
     * @returns {Array} Mock meal recommendations
     */
    async getMealRecommendations() {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve({
                    breakfast: [
                        {
                            id: 1,
                            name: "Greek Yogurt Parfait",
                            calories: 250,
                            ingredients: "Greek yogurt, granola, mixed berries",
                            allergens: "dairy, gluten"
                        },
                        {
                            id: 2,
                            name: "Avocado Toast",
                            calories: 320,
                            ingredients: "whole grain bread, avocado, tomato, seeds",
                            allergens: "gluten"
                        },
                        {
                            id: 3,
                            name: "Smoothie Bowl",
                            calories: 280,
                            ingredients: "banana, spinach, protein powder, almonds",
                            allergens: "nuts"
                        }
                    ],
                    lunch: [
                        {
                            id: 4,
                            name: "Mediterranean Bowl",
                            calories: 380,
                            ingredients: "quinoa, chickpeas, cucumber, feta, olives",
                            allergens: "dairy"
                        },
                        {
                            id: 5,
                            name: "Turkey Wrap",
                            calories: 340,
                            ingredients: "turkey breast, whole wheat wrap, vegetables",
                            allergens: "gluten"
                        },
                        {
                            id: 6,
                            name: "Lentil Soup",
                            calories: 290,
                            ingredients: "red lentils, vegetables, herbs",
                            allergens: "none"
                        }
                    ],
                    dinner: [
                        {
                            id: 7,
                            name: "Grilled Chicken & Vegetables",
                            calories: 410,
                            ingredients: "chicken breast, sweet potato, asparagus",
                            allergens: "none"
                        },
                        {
                            id: 8,
                            name: "Vegetable Stir-fry",
                            calories: 350,
                            ingredients: "tofu, mixed vegetables, brown rice",
                            allergens: "soy"
                        },
                        {
                            id: 9,
                            name: "Baked Fish with Herbs",
                            calories: 390,
                            ingredients: "white fish, herbs, roasted vegetables",
                            allergens: "fish"
                        }
                    ]
                });
            }, 300);
        });
    }
}

// Create global API client instance
window.apiClient = new ApiClient();