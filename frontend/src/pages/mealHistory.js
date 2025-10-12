/**
 * Meal History Page
 * Displays user's meal history with filtering and modern card design
 */

class MealHistoryPage {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.mealData = [];
        this.filteredData = [];
        this.currentFilter = 'all';
    }

    /**
     * Initialize DOM elements
     */
    initializeElements() {
        this.elements = {
            mealHistorySection: document.getElementById('meal-history-section'),
            historyGrid: document.getElementById('meal-history-grid'),
            historyFilter: document.getElementById('history-filter'),
            historyEmpty: document.getElementById('history-empty')
        };
    }

    /**
     * Bind event listeners
     */
    bindEvents() {
        // Filter change
        this.elements.historyFilter?.addEventListener('change', (e) => {
            this.handleFilterChange(e.target.value);
        });
    }

    /**
     * Load meal history data
     */
    async loadMealHistory() {
        const user = window.apiClient?.getCurrentUser();
        if (!user) {
            window.appRouter?.navigate('login');
            return;
        }

        try {
            this.showLoading(true);
            
            // Load meal history from API
            this.mealData = await window.apiClient.getMealHistory();
            this.filteredData = [...this.mealData];
            
            this.renderMealHistory();
            
        } catch (error) {
            console.error('Failed to load meal history:', error);
            window.notificationManager.error('Failed to load meal history');
            this.showEmptyState();
        } finally {
            this.showLoading(false);
        }
    }

    /**
     * Handle filter change
     * @param {string} filterValue - Filter value
     */
    handleFilterChange(filterValue) {
        this.currentFilter = filterValue;
        
        if (filterValue === 'all') {
            this.filteredData = [...this.mealData];
        } else {
            this.filteredData = this.mealData.filter(item => 
                item.meal.type.toLowerCase() === filterValue.toLowerCase()
            );
        }
        
        this.renderMealHistory();
    }

    /**
     * Render meal history grid
     */
    renderMealHistory() {
        if (!this.elements.historyGrid) return;

        if (this.filteredData.length === 0) {
            this.showEmptyState();
            return;
        }

        this.hideEmptyState();
        
        // Sort by date (newest first)
        const sortedData = this.filteredData.sort((a, b) => 
            new Date(b.date) - new Date(a.date)
        );

        this.elements.historyGrid.innerHTML = sortedData.map(item => 
            this.createMealCard(item)
        ).join('');

        // Add fade-in animation
        const cards = this.elements.historyGrid.querySelectorAll('.meal-history-card');
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 100}ms`;
            card.classList.add('fade-in');
        });
    }

    /**
     * Create meal history card HTML
     * @param {Object} item - Meal history item
     * @returns {string} Card HTML
     */
    createMealCard(item) {
        const formattedDate = this.formatDate(item.date);
        const mealTypeColor = this.getMealTypeColor(item.meal.type);
        const placeholderImage = this.getMealImage(item.meal.name);
        
        return `
            <div class="meal-history-card">
                <div class="meal-history-date">
                    ${formattedDate.date}
                </div>
                
                <div class="meal-image-container">
                    <div class="meal-image" style="background: ${placeholderImage};">
                        <div class="meal-image-overlay">
                            <div class="meal-type ${item.meal.type}" style="background-color: ${mealTypeColor};">
                                ${item.meal.type}
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="meal-history-content">
                    <h4 class="meal-title">${this.escapeHtml(item.meal.name)}</h4>
                    
                    <div class="meal-meta">
                        <div class="meal-calories">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
                                <path d="M8 5v3l2 2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
                            </svg>
                            ${item.meal.calories} cal
                        </div>
                        <div class="meal-time">
                            ${formattedDate.time}
                        </div>
                    </div>
                    
                    <div class="meal-ingredients">
                        <p class="text-small text-muted">${this.escapeHtml(item.meal.ingredients)}</p>
                    </div>
                    
                    <div class="meal-actions">
                        <button class="btn btn-secondary btn-small" onclick="window.mealHistoryPage.reorderMeal(${item.id})">
                            Reorder
                        </button>
                        <button class="btn-icon" onclick="window.mealHistoryPage.shareMeal(${item.id})" aria-label="Share meal">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                                <path d="M12 6l-8 4v-2L2 8l2-.5V5l8 1z" fill="currentColor"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Format date for display
     * @param {string} dateString - ISO date string
     * @returns {Object} Formatted date and time
     */
    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = now - date;
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        
        let dateDisplay;
        if (diffDays === 0) {
            dateDisplay = 'Today';
        } else if (diffDays === 1) {
            dateDisplay = 'Yesterday';
        } else if (diffDays < 7) {
            dateDisplay = `${diffDays} days ago`;
        } else {
            dateDisplay = date.toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric',
                year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
            });
        }
        
        const timeDisplay = date.toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        });
        
        return {
            date: dateDisplay,
            time: timeDisplay
        };
    }

    /**
     * Get meal type color
     * @param {string} type - Meal type
     * @returns {string} Color value
     */
    getMealTypeColor(type) {
        const colors = {
            breakfast: '#FF6B35',  // Orange
            lunch: '#4ECDC4',      // Teal
            dinner: '#45B7D1',     // Blue
            snack: '#96CEB4'       // Green
        };
        
        return colors[type.toLowerCase()] || colors.lunch;
    }

    /**
     * Get meal image gradient based on meal name
     * @param {string} mealName - Name of the meal
     * @returns {string} CSS gradient
     */
    getMealImage(mealName) {
        // Create a simple gradient based on meal name for visual variety
        const hue = this.hashCode(mealName) % 360;
        return `linear-gradient(135deg, 
            hsl(${hue}, 70%, 60%) 0%, 
            hsl(${(hue + 40) % 360}, 60%, 70%) 100%)`;
    }

    /**
     * Generate hash code from string
     * @param {string} str - String to hash
     * @returns {number} Hash code
     */
    hashCode(str) {
        let hash = 0;
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        return Math.abs(hash);
    }

    /**
     * Show loading state
     * @param {boolean} loading - Loading state
     */
    showLoading(loading) {
        if (!this.elements.historyGrid) return;

        if (loading) {
            this.elements.historyGrid.innerHTML = this.createLoadingCards();
        }
    }

    /**
     * Create loading skeleton cards
     * @returns {string} Loading cards HTML
     */
    createLoadingCards() {
        const loadingCard = `
            <div class="meal-history-card loading-card">
                <div class="loading-skeleton loading-date"></div>
                <div class="loading-skeleton loading-image"></div>
                <div class="meal-history-content">
                    <div class="loading-skeleton loading-title"></div>
                    <div class="loading-skeleton loading-meta"></div>
                    <div class="loading-skeleton loading-ingredients"></div>
                </div>
            </div>
        `;
        
        return Array(6).fill(loadingCard).join('');
    }

    /**
     * Show empty state
     */
    showEmptyState() {
        this.elements.historyGrid.innerHTML = '';
        this.elements.historyEmpty?.classList.remove('hidden');
        
        // Update empty state message based on filter
        const emptyTitle = this.elements.historyEmpty?.querySelector('h3');
        const emptyMessage = this.elements.historyEmpty?.querySelector('p');
        
        if (this.currentFilter === 'all') {
            if (emptyTitle) emptyTitle.textContent = 'No meal history yet';
            if (emptyMessage) emptyMessage.textContent = 'Start tracking your meals to see your nutrition journey here';
        } else {
            if (emptyTitle) emptyTitle.textContent = `No ${this.currentFilter} meals found`;
            if (emptyMessage) emptyMessage.textContent = `You haven't logged any ${this.currentFilter} meals yet`;
        }
    }

    /**
     * Hide empty state
     */
    hideEmptyState() {
        this.elements.historyEmpty?.classList.add('hidden');
    }

    /**
     * Reorder a meal
     * @param {number} mealId - Meal ID to reorder
     */
    reorderMeal(mealId) {
        const meal = this.mealData.find(item => item.id === mealId);
        if (!meal) return;

        window.notificationManager.info(`Reordering "${meal.meal.name}" - this feature will be implemented in Sprint 3`);
        
        // In a real implementation, this would:
        // 1. Add the meal to today's plan
        // 2. Navigate to meal recommendations
        // 3. Show confirmation
    }

    /**
     * Share a meal
     * @param {number} mealId - Meal ID to share
     */
    shareMeal(mealId) {
        const meal = this.mealData.find(item => item.id === mealId);
        if (!meal) return;

        // Simple share functionality using Web Share API or fallback
        if (navigator.share) {
            navigator.share({
                title: `I enjoyed ${meal.meal.name}`,
                text: `Check out this healthy meal: ${meal.meal.name} (${meal.meal.calories} calories)`,
                url: window.location.href
            }).catch(err => {
                console.log('Error sharing:', err);
                this.fallbackShare(meal);
            });
        } else {
            this.fallbackShare(meal);
        }
    }

    /**
     * Fallback share method
     * @param {Object} meal - Meal data
     */
    fallbackShare(meal) {
        const text = `I enjoyed ${meal.meal.name} (${meal.meal.calories} calories) - ${meal.meal.ingredients}`;
        
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text);
            window.notificationManager.success('Meal details copied to clipboard!');
        } else {
            window.notificationManager.info('Share feature available in modern browsers');
        }
    }

    /**
     * Escape HTML to prevent XSS
     * @param {string} text - Text to escape
     * @returns {string} Escaped text
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    /**
     * Show meal history section
     */
    show() {
        this.elements.mealHistorySection?.classList.remove('hidden');
        this.loadMealHistory();
    }

    /**
     * Hide meal history section
     */
    hide() {
        this.elements.mealHistorySection?.classList.add('hidden');
    }

    /**
     * Refresh meal history
     */
    refresh() {
        this.loadMealHistory();
    }
}

// Add meal history-specific styles
const mealHistoryStyles = `
.meal-history-card {
    background-color: var(--surface-color);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow);
    overflow: hidden;
    transition: all var(--transition-normal);
    animation: fadeIn var(--transition-normal) ease-out both;
}

.meal-history-card:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-4px);
}

.meal-history-date {
    background-color: var(--primary-color-light);
    color: var(--primary-color-dark);
    padding: var(--spacing-sm) var(--spacing-base);
    font-size: var(--font-size-xs);
    font-weight: var(--font-weight-semibold);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-align: center;
}

.meal-image-container {
    position: relative;
    height: 160px;
    overflow: hidden;
}

.meal-image {
    width: 100%;
    height: 100%;
    position: relative;
    background-size: cover;
    background-position: center;
}

.meal-image-overlay {
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(transparent, rgba(0, 0, 0, 0.3));
    padding: var(--spacing-base);
    display: flex;
    justify-content: flex-end;
}

.meal-type {
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--border-radius);
    color: white;
    font-size: var(--font-size-xs);
    font-weight: var(--font-weight-semibold);
    text-transform: capitalize;
}

.meal-history-content {
    padding: var(--spacing-base);
}

.meal-title {
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-semibold);
    margin-bottom: var(--spacing-sm);
    color: var(--text-primary-color);
    line-height: var(--line-height-tight);
}

.meal-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--spacing-sm);
}

.meal-calories {
    display: flex;
    align-items: center;
    gap: var(--spacing-xs);
    background-color: var(--success-color-light);
    color: var(--success-color);
    padding: var(--spacing-xs) var(--spacing-sm);
    border-radius: var(--border-radius);
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-medium);
}

.meal-time {
    color: var(--text-muted-color);
    font-size: var(--font-size-sm);
}

.meal-ingredients {
    margin-bottom: var(--spacing-base);
}

.meal-ingredients p {
    margin-bottom: 0;
    line-height: var(--line-height-relaxed);
}

.meal-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: var(--spacing-sm);
}

/* Loading states */
.loading-card .loading-skeleton {
    background: linear-gradient(90deg, 
        var(--secondary-color) 25%, 
        var(--border-color-light) 50%, 
        var(--secondary-color) 75%
    );
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
    border-radius: var(--border-radius-sm);
}

.loading-date {
    height: 24px;
    margin-bottom: var(--spacing-sm);
}

.loading-image {
    height: 160px;
    margin-bottom: var(--spacing-base);
}

.loading-title {
    height: 24px;
    width: 80%;
    margin-bottom: var(--spacing-sm);
}

.loading-meta {
    height: 20px;
    width: 60%;
    margin-bottom: var(--spacing-sm);
}

.loading-ingredients {
    height: 16px;
    width: 100%;
}

@keyframes loading {
    0% {
        background-position: -200% 0;
    }
    100% {
        background-position: 200% 0;
    }
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .meal-history-grid {
        grid-template-columns: 1fr;
        gap: var(--spacing-base);
    }
    
    .meal-actions {
        flex-direction: column;
        gap: var(--spacing-sm);
    }
    
    .meal-actions .btn {
        width: 100%;
    }
}

@media (max-width: 480px) {
    .meal-image-container {
        height: 120px;
    }
    
    .meal-history-content {
        padding: var(--spacing-sm);
    }
}
`;

// Inject styles
const mealHistoryStyleSheet = document.createElement('style');
mealHistoryStyleSheet.textContent = mealHistoryStyles;
document.head.appendChild(mealHistoryStyleSheet);

// Create global meal history page instance
window.mealHistoryPage = new MealHistoryPage();