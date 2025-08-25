// Main JavaScript for Workflow System

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        if (!alert.classList.contains('alert-danger')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });

    // Confirm delete actions
    const deleteButtons = document.querySelectorAll('[href*="delete"]');
    deleteButtons.forEach(button => {
        if (button.getAttribute('href').includes('delete') && !button.classList.contains('btn-danger')) {
            button.addEventListener('click', function(e) {
                if (!confirm('Are you sure you want to delete this item?')) {
                    e.preventDefault();
                }
            });
        }
    });

    // Enhanced status update functionality
    const statusSelects = document.querySelectorAll('.status-select');
    statusSelects.forEach(select => {
        const originalValue = select.value;
        
        select.addEventListener('change', function() {
            const taskId = this.dataset.taskId;
            const newStatus = this.value;
            const selectElement = this;
            
            // Add loading state
            selectElement.classList.add('loading');
            selectElement.disabled = true;
            
            fetch(`/tasks/${taskId}/status/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({status: newStatus})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showNotification('Status updated successfully!', 'success');
                    // Update any badges on the page
                    updateStatusBadges(taskId, newStatus);
                } else {
                    showNotification('Failed to update status: ' + data.message, 'danger');
                    // Revert to original value
                    selectElement.value = originalValue;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showNotification('An error occurred while updating status', 'danger');
                selectElement.value = originalValue;
            })
            .finally(() => {
                // Remove loading state
                selectElement.classList.remove('loading');
                selectElement.disabled = false;
            });
        });
    });

    // Search functionality enhancement
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                // Auto-submit search after 500ms of no typing
                if (this.value.length >= 3 || this.value.length === 0) {
                    this.closest('form').submit();
                }
            }, 500);
        });
    }
});

// Helper function to get CSRF token
function getCookie(name) {
    // Try to get from meta tag first
    const metaToken = document.querySelector('meta[name="csrf-token"]');
    if (metaToken) {
        return metaToken.getAttribute('content');
    }
    
    // Fallback to cookie method
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Helper function to show notifications
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 1050; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }
    }, 5000);
}

// Helper function to update status badges
function updateStatusBadges(taskId, newStatus) {
    const badges = document.querySelectorAll(`[data-task-id="${taskId}"] .badge, .badge[data-task-id="${taskId}"]`);
    badges.forEach(badge => {
        // Update badge text
        const statusLabels = {
            'pending': 'Pending',
            'in_progress': 'In Progress',
            'completed': 'Completed',
            'cancelled': 'Cancelled'
        };
        badge.textContent = statusLabels[newStatus] || newStatus;
        
        // Update badge class
        badge.className = badge.className.replace(/bg-\w+/, '');
        const statusClasses = {
            'pending': 'bg-warning',
            'in_progress': 'bg-info',
            'completed': 'bg-success',
            'cancelled': 'bg-danger'
        };
        badge.classList.add(statusClasses[newStatus] || 'bg-secondary');
    });
}

// Form validation enhancement
document.addEventListener('submit', function(e) {
    const form = e.target;
    if (form.classList.contains('needs-validation')) {
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
        }
        form.classList.add('was-validated');
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl+N or Cmd+N to create new task (when not in input field)
    if ((e.ctrlKey || e.metaKey) && e.key === 'n' && !e.target.matches('input, textarea, select')) {
        e.preventDefault();
        const createButton = document.querySelector('[href*="create"]');
        if (createButton) {
            window.location.href = createButton.href;
        }
    }
    
    // Escape key to go back or close modals
    if (e.key === 'Escape') {
        const modal = document.querySelector('.modal.show');
        if (modal) {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) bsModal.hide();
        } else {
            const backButton = document.querySelector('.btn-secondary[href*="back"], .btn-secondary[href*="list"]');
            if (backButton) {
                window.location.href = backButton.href;
            }
        }
    }
});
