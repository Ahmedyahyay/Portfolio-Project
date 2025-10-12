/**
 * Notification System
 * Handles user notifications and alerts
 */

class NotificationManager {
    constructor() {
        this.container = document.getElementById('notifications');
        this.notifications = new Map();
        this.counter = 0;
    }

    /**
     * Show a notification
     * @param {string} message - Notification message
     * @param {string} type - Notification type (success, error, warning, info)
     * @param {number} duration - Auto-dismiss duration in ms (0 for persistent)
     * @returns {string} Notification ID
     */
    show(message, type = 'info', duration = 5000) {
        const id = `notification-${++this.counter}`;
        const notification = this.createNotification(id, message, type);
        
        this.container.appendChild(notification);
        this.notifications.set(id, notification);
        
        // Animate in
        requestAnimationFrame(() => {
            notification.classList.add('fade-in');
        });
        
        // Auto-dismiss
        if (duration > 0) {
            setTimeout(() => {
                this.dismiss(id);
            }, duration);
        }
        
        return id;
    }

    /**
     * Create notification element
     * @param {string} id - Notification ID
     * @param {string} message - Message text
     * @param {string} type - Notification type
     * @returns {HTMLElement} Notification element
     */
    createNotification(id, message, type) {
        const notification = document.createElement('div');
        notification.id = id;
        notification.className = `notification ${type}`;
        notification.setAttribute('role', 'alert');
        notification.setAttribute('aria-live', 'polite');
        
        const icon = this.getIcon(type);
        const dismissButton = this.createDismissButton(id);
        
        notification.innerHTML = `
            <div class="notification-content flex items-start gap-4">
                <div class="notification-icon">
                    ${icon}
                </div>
                <div class="notification-message flex-1">
                    ${this.escapeHtml(message)}
                </div>
                ${dismissButton}
            </div>
        `;
        
        return notification;
    }

    /**
     * Create dismiss button
     * @param {string} id - Notification ID
     * @returns {string} Button HTML
     */
    createDismissButton(id) {
        return `
            <button 
                class="notification-dismiss btn-icon" 
                onclick="window.notificationManager.dismiss('${id}')"
                aria-label="Dismiss notification"
            >
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                    <path d="M12 4L4 12M4 4l8 8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                </svg>
            </button>
        `;
    }

    /**
     * Get icon for notification type
     * @param {string} type - Notification type
     * @returns {string} Icon SVG
     */
    getIcon(type) {
        const icons = {
            success: `
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <circle cx="10" cy="10" r="9" fill="var(--success-color)"/>
                    <path d="M6 10l2 2 6-6" stroke="white" stroke-width="2" stroke-linecap="round"/>
                </svg>
            `,
            error: `
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <circle cx="10" cy="10" r="9" fill="var(--error-color)"/>
                    <path d="M7 7l6 6M13 7l-6 6" stroke="white" stroke-width="2" stroke-linecap="round"/>
                </svg>
            `,
            warning: `
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <circle cx="10" cy="10" r="9" fill="var(--warning-color)"/>
                    <path d="M10 6v4M10 14h.01" stroke="white" stroke-width="2" stroke-linecap="round"/>
                </svg>
            `,
            info: `
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                    <circle cx="10" cy="10" r="9" fill="var(--info-color)"/>
                    <path d="M10 14V10M10 6h.01" stroke="white" stroke-width="2" stroke-linecap="round"/>
                </svg>
            `
        };
        
        return icons[type] || icons.info;
    }

    /**
     * Dismiss a notification
     * @param {string} id - Notification ID
     */
    dismiss(id) {
        const notification = this.notifications.get(id);
        if (!notification) return;
        
        notification.style.transform = 'translateX(100%)';
        notification.style.opacity = '0';
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
            this.notifications.delete(id);
        }, 300);
    }

    /**
     * Dismiss all notifications
     */
    dismissAll() {
        this.notifications.forEach((_, id) => {
            this.dismiss(id);
        });
    }

    /**
     * Show success notification
     * @param {string} message - Success message
     * @param {number} duration - Auto-dismiss duration
     */
    success(message, duration = 5000) {
        return this.show(message, 'success', duration);
    }

    /**
     * Show error notification
     * @param {string} message - Error message
     * @param {number} duration - Auto-dismiss duration (0 for persistent)
     */
    error(message, duration = 8000) {
        return this.show(message, 'error', duration);
    }

    /**
     * Show warning notification
     * @param {string} message - Warning message
     * @param {number} duration - Auto-dismiss duration
     */
    warning(message, duration = 6000) {
        return this.show(message, 'warning', duration);
    }

    /**
     * Show info notification
     * @param {string} message - Info message
     * @param {number} duration - Auto-dismiss duration
     */
    info(message, duration = 5000) {
        return this.show(message, 'info', duration);
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
}

// Add CSS for notification components
const notificationStyles = `
.notification-content {
    align-items: flex-start;
}

.notification-icon {
    flex-shrink: 0;
}

.notification-message {
    color: var(--text-primary-color);
    font-size: var(--font-size-sm);
    line-height: var(--line-height-relaxed);
}

.notification-dismiss {
    background: none;
    border: none;
    color: var(--text-muted-color);
    cursor: pointer;
    padding: var(--spacing-xs);
    border-radius: var(--border-radius-sm);
    transition: all var(--transition-fast);
    flex-shrink: 0;
}

.notification-dismiss:hover {
    color: var(--text-primary-color);
    background-color: var(--secondary-color);
}

.btn-icon {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
}
`;

// Inject styles
const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet);

// Create global notification manager instance
window.notificationManager = new NotificationManager();