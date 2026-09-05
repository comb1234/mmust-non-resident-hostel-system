// Main JavaScript file with shared utilities

// Toggle password visibility
function togglePassword(inputId, icon) {
    const input = document.getElementById(inputId);
    if (input.type === 'password') {
        input.type = 'text';
        icon.innerHTML = '<i class="fas fa-eye-slash"></i>';
    } else {
        input.type = 'password';
        icon.innerHTML = '<i class="fas fa-eye"></i>';
    }
}

// Format date for display
function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-KE', { year: 'numeric', month: 'short', day: 'numeric' });
}

// Format currency
function formatCurrency(amount) {
    return 'KSh ' + Number(amount).toLocaleString();
}

// Mobile nav toggle
document.addEventListener('DOMContentLoaded', function() {
    const navToggle = document.getElementById('navToggle');
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            document.getElementById('navLinks').classList.toggle('active');
        });
    }
    // Sidebar toggle for dashboard pages
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            document.querySelector('.sidebar').classList.toggle('open');
        });
    }
    // Logout button handler
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            Auth.logout();
        });
    }
});

// Offline/connection detection and UI adjustments
(function detectOfflineMode() {
    async function markOffline(reason) {
        try {
            document.body.classList.add('offline-mode');
            // Inject a subtle banner under the navbar
            const existing = document.getElementById('offlineBanner');
            if (existing) {
                existing.textContent = reason;
                return;
            }
            const nav = document.querySelector('.navbar');
            const banner = document.createElement('div');
            banner.id = 'offlineBanner';
            banner.className = 'offline-banner';
            banner.textContent = reason;
            if (nav && nav.parentNode) nav.parentNode.insertBefore(banner, nav.nextSibling);
            else document.body.insertBefore(banner, document.body.firstChild);
        } catch (e) { /* ignore */ }
    }

    try {
        if (location.protocol === 'file:') {
            markOffline('Offline mode: opened via file:// — using local data and mock auth');
            return;
        }
    } catch (e) {}

    // Try to reach a known backend endpoint (/api/hostels/); handle 404 vs unreachable
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 2500);
    const apiHost = API_BASE_URL.replace(/\/api\/?$/, '');
    const probeUrl = apiHost + '/api/hostels/';
    fetch(probeUrl, { method: 'GET', signal: controller.signal })
        .then(resp => {
            clearTimeout(timeout);
            if (!resp.ok) markOffline(`Online — backend responded ${resp.status} at probe endpoint`);
        })
        .catch(() => {
            clearTimeout(timeout);
            markOffline(`Offline mode: backend unreachable at ${apiHost}`);
        });
})();