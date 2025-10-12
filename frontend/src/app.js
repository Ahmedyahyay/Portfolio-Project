/**
 * Main Application Controller
 * Handles routing, initialization, and app state management
 */

class AppRouter {
    constructor() {
        this.currentPage = 'home';
        this.isInitialized = false;
        this.initializeApp();
    }

    /**
     * Initialize the application
     */
    initializeApp() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.init());
        } else {
            this.init();
        }
    }

    /**
     * Initialize app components
     */
    init() {
        // Initialize routing
        this.setupRouting();
        
        // Initialize scroll effects
        this.setupScrollEffects();
        
        // Check authentication state
        this.checkAuthState();
        
        // Navigate to initial page
        this.navigateFromURL();
        
        // Setup hero section interactions
        this.setupHeroInteractions();
        
        // Setup dashboard interactions
        this.setupDashboardInteractions();
        
        this.isInitialized = true;
        console.log('Personal Nutrition Assistant initialized successfully');
    }

    /**
     * Setup routing system
     */
    setupRouting() {
        // Handle browser back/forward
        window.addEventListener('popstate', () => {
            this.navigateFromURL();
        });
        
        // Handle hash changes
        window.addEventListener('hashchange', () => {
            this.navigateFromURL();
        });
    }

    /**
     * Setup scroll effects
     */
    setupScrollEffects() {
        let lastScroll = 0;
        const header = document.getElementById('header');
        
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            // Add scrolled class to header
            if (currentScroll > 50) {
                header?.classList.add('scrolled');
            } else {
                header?.classList.remove('scrolled');
            }
            
            lastScroll = currentScroll;
        });
    }

    /**
     * Setup hero section interactions
     */
    setupHeroInteractions() {
        const heroSection = document.getElementById('hero-section');
        const heroCTA = document.getElementById('hero-cta');
        const learnMore = document.getElementById('learn-more');

        // Hero CTA button
        heroCTA?.addEventListener('click', () => {
            if (window.apiClient?.isAuthenticated()) {
                this.navigate('dashboard');
            } else {
                this.navigate('register');
            }
        });

        // Learn more button - smooth scroll to content
        learnMore?.addEventListener('click', () => {
            const appContainer = document.getElementById('app-container');
            if (appContainer) {
                appContainer.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });

        // Add parallax effect to hero background (subtle)
        if (heroSection) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const parallaxSpeed = 0.5;
                heroSection.style.transform = `translateY(${scrolled * parallaxSpeed}px)`;
            });
        }
    }

    /**
     * Setup dashboard interactions
     */
    setupDashboardInteractions() {
        const manageProfile = document.getElementById('manage-profile');
        const viewHistory = document.getElementById('view-history');

        manageProfile?.addEventListener('click', () => {
            this.navigate('profile');
        });

        viewHistory?.addEventListener('click', () => {
            this.navigate('meals');
        });
    }

    /**
     * Check authentication state and update UI
     */
    checkAuthState() {
        const isAuthenticated = window.apiClient?.isAuthenticated();
        const user = window.apiClient?.getCurrentUser();

        if (isAuthenticated && user) {
            // Update navbar
            window.navbarManager?.showUserMenu(user);
            
            // Update dashboard BMI if user data available
            this.updateDashboardBMI();
        } else {
            window.navbarManager?.showAuthMenu();
        }
    }

    /**
     * Update dashboard BMI display
     */
    updateDashboardBMI() {
        // This would normally get user data from the API
        // For now, we'll use placeholder data or profile data if available
        const userData = window.profilePage?.getCurrentUserData();
        
        if (userData && userData.height && userData.weight) {
            const bmiData = window.authManager.calculateBMI(userData.height, userData.weight);
            
            const bmiDisplay = document.getElementById('bmi-display');
            const bmiStatus = document.getElementById('bmi-status');
            
            if (bmiDisplay) {
                bmiDisplay.textContent = `BMI: ${bmiData.bmi}`;
            }
            
            if (bmiStatus) {
                const eligibilityClass = bmiData.isEligible ? 'bmi-status--eligible' : 'bmi-status--ineligible';
                const eligibilityText = bmiData.isEligible ? '✓ Eligible for Program' : '⚠ Below Program Threshold';
                
                bmiStatus.className = `bmi-status ${eligibilityClass}`;
                bmiStatus.innerHTML = `<span>${eligibilityText}</span>`;
                bmiStatus.classList.remove('hidden');
            }
        }
    }

    /**
     * Navigate to a page
     * @param {string} page - Page name
     * @param {boolean} pushState - Whether to update browser history
     */
    navigate(page, pushState = true) {
        // Validate page
        const validPages = ['home', 'login', 'register', 'dashboard', 'profile', 'meals', 'recommendations'];
        if (!validPages.includes(page)) {
            console.warn(`Invalid page: ${page}`);
            page = 'home';
        }

        // Check authentication requirements
        const protectedPages = ['dashboard', 'profile', 'meals', 'recommendations'];
        if (protectedPages.includes(page) && !window.apiClient?.isAuthenticated()) {
            window.notificationManager.warning('Please log in to access this feature');
            page = 'login';
        }

        // Update browser history
        if (pushState && page !== this.currentPage) {
            const url = page === 'home' ? '/' : `/#${page}`;
            history.pushState({ page }, '', url);
        }

        // Update current page
        this.currentPage = page;
        
        // Hide all sections first
        this.hideAllSections();
        
        // Show requested section
        this.showSection(page);
        
        // Update navbar active state
        window.navbarManager?.highlightSection(page);
        
        // Page-specific actions
        this.handlePageSpecificActions(page);
    }

    /**
     * Navigate from current URL
     */
    navigateFromURL() {
        const hash = window.location.hash.substring(1);
        const page = hash || 'home';
        this.navigate(page, false);
    }

    /**
     * Hide all page sections
     */
    hideAllSections() {
        const sections = [
            'dashboard',
            'auth-container', 
            'profile-section',
            'meal-history-section'
        ];

        sections.forEach(sectionId => {
            const section = document.getElementById(sectionId);
            section?.classList.add('hidden');
        });
    }

    /**
     * Show specific section
     * @param {string} page - Page to show
     */
    showSection(page) {
        const heroSection = document.getElementById('hero-section');
        
        switch (page) {
            case 'home':
            case 'dashboard':
                heroSection?.classList.remove('hidden');
                if (window.apiClient?.isAuthenticated()) {
                    this.showDashboard();
                } else {
                    this.showHero();
                }
                break;
                
            case 'login':
                heroSection?.classList.add('hidden');
                window.authPages?.show();
                window.authPages?.showLoginForm();
                break;
                
            case 'register':
                heroSection?.classList.add('hidden');
                window.authPages?.show();
                window.authPages?.showRegisterForm();
                break;
                
            case 'profile':
                heroSection?.classList.add('hidden');
                window.profilePage?.show();
                break;
                
            case 'meals':
                heroSection?.classList.add('hidden');
                window.mealHistoryPage?.show();
                break;
                
            case 'recommendations':
                heroSection?.classList.add('hidden');
                this.showRecommendations();
                break;
                
            default:
                this.showHero();
        }
    }

    /**
     * Show hero section
     */
    showHero() {
        const heroSection = document.getElementById('hero-section');
        const dashboard = document.getElementById('dashboard');
        
        heroSection?.classList.remove('hidden');
        dashboard?.classList.add('hidden');
    }

    /**
     * Show dashboard
     */
    showDashboard() {
        const heroSection = document.getElementById('hero-section');
        const dashboard = document.getElementById('dashboard');
        
        heroSection?.classList.add('hidden');
        dashboard?.classList.remove('hidden');
        
        // Update BMI display
        this.updateDashboardBMI();
    }

    /**
     * Show recommendations (placeholder)
     */
    showRecommendations() {
        window.notificationManager.info('Meal recommendations feature will be implemented in Sprint 3');
        this.navigate('dashboard');
    }

    /**
     * Handle page-specific actions
     * @param {string} page - Current page
     */
    handlePageSpecificActions(page) {
        // Update page title
        this.updatePageTitle(page);
        
        // Track page view (analytics placeholder)
        this.trackPageView(page);
        
        // Focus management for accessibility
        this.manageFocus(page);
    }

    /**
     * Update page title
     * @param {string} page - Current page
     */
    updatePageTitle(page) {
        const titles = {
            home: 'Personal Nutrition Assistant - Your Path to Healthier Living',
            dashboard: 'Dashboard - Personal Nutrition Assistant',
            login: 'Login - Personal Nutrition Assistant',
            register: 'Register - Personal Nutrition Assistant',
            profile: 'Profile - Personal Nutrition Assistant',
            meals: 'Meal History - Personal Nutrition Assistant',
            recommendations: 'Recommendations - Personal Nutrition Assistant'
        };
        
        document.title = titles[page] || titles.home;
    }

    /**
     * Track page view (analytics placeholder)
     * @param {string} page - Page name
     */
    trackPageView(page) {
        // Placeholder for analytics tracking
        console.log(`Page view: ${page}`);
    }

    /**
     * Manage focus for accessibility
     * @param {string} page - Current page
     */
    manageFocus(page) {
        // Focus main content for screen readers
        const mainContent = document.getElementById('main-content');
        if (mainContent) {
            mainContent.focus({ preventScroll: true });
        }
    }

    /**
     * Get current page
     * @returns {string} Current page name
     */
    getCurrentPage() {
        return this.currentPage;
    }

    /**
     * Check if app is initialized
     * @returns {boolean} Initialization status
     */
    isReady() {
        return this.isInitialized;
    }
}

// Global error handler
window.addEventListener('error', (event) => {
    console.error('Application error:', event.error);
    
    if (window.notificationManager) {
        window.notificationManager.error('An unexpected error occurred. Please refresh the page.');
    }
});

// Global unhandled promise rejection handler
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    
    if (window.notificationManager) {
        window.notificationManager.error('A network error occurred. Please check your connection.');
    }
});

// Initialize app when script loads
window.appRouter = new AppRouter();

// Export for global access
window.NutritionApp = {
    router: window.appRouter,
    api: window.apiClient,
    auth: window.authManager,
    notifications: window.notificationManager,
    version: '2.0.0'
};

// Development helpers (remove in production)
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    window.dev = {
        testLogin: () => {
            window.apiClient.currentUser = { id: 1, email: 'test@example.com' };
            window.authManager.triggerLogin(window.apiClient.currentUser);
            window.appRouter.navigate('dashboard');
        },
        testLogout: () => {
            window.apiClient.logout();
            window.authManager.triggerLogout();
            window.appRouter.navigate('home');
        },
        showNotification: (type = 'info', message = 'Test notification') => {
            window.notificationManager[type](message);
        }
    };
    
    console.log('Development mode active. Use window.dev for testing utilities.');
}