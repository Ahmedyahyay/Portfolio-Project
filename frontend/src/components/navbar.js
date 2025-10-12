/**
 * Navigation Bar Component
 * Handles navigation state and user interface
 */

class NavbarManager {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.updateAuthState();
        
        // Listen for auth state changes
        window.authManager.onLogin(user => this.handleLogin(user));
        window.authManager.onLogout(() => this.handleLogout());
    }

    /**
     * Initialize DOM elements
     */
    initializeElements() {
        this.elements = {
            authMenu: document.getElementById('auth-menu'),
            userMenu: document.getElementById('user-menu'),
            userName: document.getElementById('user-name'),
            loginBtn: document.getElementById('login-btn'),
            registerBtn: document.getElementById('register-btn'),
            logoutBtn: document.getElementById('logout-btn'),
            mobileMenuBtn: document.getElementById('mobile-menu-btn'),
            mobileMenu: document.getElementById('mobile-menu'),
            navLinks: document.querySelectorAll('.nav-link, .mobile-nav-link')
        };
    }

    /**
     * Bind event listeners
     */
    bindEvents() {
        // Auth buttons
        this.elements.loginBtn?.addEventListener('click', () => this.showLogin());
        this.elements.registerBtn?.addEventListener('click', () => this.showRegister());
        this.elements.logoutBtn?.addEventListener('click', () => this.handleLogout());

        // Mobile menu toggle
        this.elements.mobileMenuBtn?.addEventListener('click', () => this.toggleMobileMenu());

        // Navigation links
        this.elements.navLinks.forEach(link => {
            link.addEventListener('click', (e) => this.handleNavigation(e));
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.navbar') && !this.elements.mobileMenu.classList.contains('hidden')) {
                this.closeMobileMenu();
            }
        });

        // Handle escape key for mobile menu
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && !this.elements.mobileMenu.classList.contains('hidden')) {
                this.closeMobileMenu();
            }
        });
    }

    /**
     * Update authentication state in navbar
     */
    updateAuthState() {
        const isAuthenticated = window.apiClient?.isAuthenticated();
        const user = window.apiClient?.getCurrentUser();

        if (isAuthenticated && user) {
            this.showUserMenu(user);
        } else {
            this.showAuthMenu();
        }
    }

    /**
     * Show user menu (authenticated state)
     * @param {Object} user - User data
     */
    showUserMenu(user) {
        this.elements.authMenu?.classList.add('hidden');
        this.elements.userMenu?.classList.remove('hidden');
        
        if (this.elements.userName) {
            this.elements.userName.textContent = user.email.split('@')[0] || 'User';
        }
    }

    /**
     * Show auth menu (unauthenticated state)
     */
    showAuthMenu() {
        this.elements.userMenu?.classList.add('hidden');
        this.elements.authMenu?.classList.remove('hidden');
    }

    /**
     * Handle login event
     * @param {Object} user - User data
     */
    handleLogin(user) {
        this.showUserMenu(user);
        this.closeMobileMenu();
        window.notificationManager.success(`Welcome back, ${user.email.split('@')[0]}!`);
    }

    /**
     * Handle logout event
     */
    handleLogout() {
        window.apiClient?.logout();
        this.showAuthMenu();
        this.closeMobileMenu();
        
        // Navigate to home
        window.appRouter?.navigate('home');
        window.notificationManager.info('You have been logged out');
    }

    /**
     * Show login form
     */
    showLogin() {
        window.appRouter?.navigate('login');
        this.closeMobileMenu();
    }

    /**
     * Show registration form
     */
    showRegister() {
        window.appRouter?.navigate('register');
        this.closeMobileMenu();
    }

    /**
     * Toggle mobile menu
     */
    toggleMobileMenu() {
        const isHidden = this.elements.mobileMenu.classList.contains('hidden');
        
        if (isHidden) {
            this.openMobileMenu();
        } else {
            this.closeMobileMenu();
        }
    }

    /**
     * Open mobile menu
     */
    openMobileMenu() {
        this.elements.mobileMenu?.classList.remove('hidden');
        this.elements.mobileMenuBtn?.setAttribute('aria-expanded', 'true');
        
        // Focus first menu item for accessibility
        const firstLink = this.elements.mobileMenu.querySelector('.mobile-nav-link');
        firstLink?.focus();
    }

    /**
     * Close mobile menu
     */
    closeMobileMenu() {
        this.elements.mobileMenu?.classList.add('hidden');
        this.elements.mobileMenuBtn?.setAttribute('aria-expanded', 'false');
    }

    /**
     * Handle navigation clicks
     * @param {Event} e - Click event
     */
    handleNavigation(e) {
        e.preventDefault();
        const href = e.target.getAttribute('href');
        
        if (href && href.startsWith('#')) {
            const page = href.substring(1);
            window.appRouter?.navigate(page);
            this.closeMobileMenu();
            this.updateActiveLink(page);
        }
    }

    /**
     * Update active navigation link
     * @param {string} page - Current page
     */
    updateActiveLink(page) {
        this.elements.navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === `#${page}`) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    }

    /**
     * Set loading state for navbar
     * @param {boolean} loading - Loading state
     */
    setLoading(loading) {
        const buttons = [this.elements.loginBtn, this.elements.registerBtn, this.elements.logoutBtn];
        
        buttons.forEach(btn => {
            if (btn) {
                if (loading) {
                    btn.classList.add('loading');
                    btn.disabled = true;
                } else {
                    btn.classList.remove('loading');
                    btn.disabled = false;
                }
            }
        });
    }

    /**
     * Highlight navigation item
     * @param {string} section - Section to highlight
     */
    highlightSection(section) {
        this.updateActiveLink(section);
    }
}

// Add navbar-specific styles
const navbarStyles = `
.navbar {
    transition: all var(--transition-normal);
}

.navbar.scrolled {
    background-color: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
}

.mobile-menu {
    animation: slideDown var(--transition-fast) ease-out;
}

@keyframes slideDown {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.user-menu {
    align-items: center;
    gap: var(--spacing-base);
}

@media (max-width: 767px) {
    .mobile-nav-link {
        display: block;
        padding: var(--spacing-sm) var(--spacing-base);
        border-radius: var(--border-radius);
        transition: background-color var(--transition-fast);
    }
    
    .mobile-nav-link:hover {
        background-color: var(--secondary-color);
    }
}
`;

// Inject styles
const navbarStyleSheet = document.createElement('style');
navbarStyleSheet.textContent = navbarStyles;
document.head.appendChild(navbarStyleSheet);

// Create global navbar manager instance
window.navbarManager = new NavbarManager();