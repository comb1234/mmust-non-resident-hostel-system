// API Service Module – handles all HTTP requests to Django backend
const API = {
    // Get JWT token from localStorage
    getToken() {
        return localStorage.getItem('access_token');
    },
    // Set JWT token
    setToken(token) {
        localStorage.setItem('access_token', token);
    },
    // Helper for authenticated fetch requests
    async authFetch(url, options = {}) {
        const token = this.getToken();
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };
        if (token) headers['Authorization'] = `Bearer ${token}`;
        try {
            const response = await fetch(`${API_BASE_URL}${url}`, { ...options, headers });
            if (response.status === 401) {
                localStorage.removeItem('access_token');
                localStorage.removeItem('refresh_token');
                window.location.href = '../login.html';
                throw new Error('Unauthorized');
            }
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || errorData.error || 'API request failed');
            }
            return response.json();
        } catch (err) {
            if (err instanceof TypeError) throw new Error(`Network error: cannot reach backend at ${API_BASE_URL}`);
            throw err;
        }
    },
    // Authentication endpoints
    async register(userData) {
        if (location.protocol === 'file:') {
            // Offline: create a mock user locally for testing
            const users = JSON.parse(localStorage.getItem('mock_users') || '[]');
            const exists = users.find(u => u.email === userData.email);
            if (exists) throw new Error('User already exists (offline)');
            const user = { id: Date.now(), email: userData.email, role: 'student', first_name: userData.first_name, last_name: userData.last_name };
            users.push({ ...user, password: userData.password });
            localStorage.setItem('mock_users', JSON.stringify(users));
            // Set a fake token
            this.setToken('offline-token');
            localStorage.setItem('refresh_token', 'offline-refresh');
            return user;
        }
        try {
            const response = await fetch(`${API_BASE_URL}/auth/register/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(userData),
            });
            const data = await response.json();
            if (!response.ok) throw new Error(JSON.stringify(data));
            this.setToken(data.access);
            localStorage.setItem('refresh_token', data.refresh);
            return data.user;
        } catch (err) {
            if (err instanceof TypeError) throw new Error(`Network error: cannot reach backend at ${API_BASE_URL}`);
            throw err;
        }
    },
    async login(email, password) {
        if (location.protocol === 'file:') {
            // Offline mock login: accept the seeded admin or mock users
            if (email === 'admin@mmust.ac.ke' && password === 'mmust1234') {
                const admin = { id: 0, email, role: 'admin', first_name: 'MMUST', last_name: 'Admin' };
                this.setToken('offline-admin-token');
                localStorage.setItem('refresh_token', 'offline-refresh');
                return admin;
            }
            const users = JSON.parse(localStorage.getItem('mock_users') || '[]');
            const found = users.find(u => u.email === email && u.password === password);
            if (found) {
                const user = { id: found.id, email: found.email, role: 'student', first_name: found.first_name, last_name: found.last_name };
                this.setToken('offline-token');
                localStorage.setItem('refresh_token', 'offline-refresh');
                return user;
            }
            throw new Error('Invalid credentials (offline)');
        }
        try {
            const response = await fetch(`${API_BASE_URL}/auth/login/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Login failed');
            this.setToken(data.access);
            localStorage.setItem('refresh_token', data.refresh);
            return data.user;
        } catch (err) {
            if (err instanceof TypeError) throw new Error(`Network error: cannot reach backend at ${API_BASE_URL}`);
            throw err;
        }
    },
    async getCurrentUser() {
        return this.authFetch('/auth/profile/');
    },
    async updateProfile(userData) {
        return this.authFetch('/auth/profile/', { method: 'PATCH', body: JSON.stringify(userData) });
    },
    // Hostels (public)
    async getHostels(params = '') {
        // If running from file:// (double-clicking index.html), fall back to local JSON or embedded data
        if (location.protocol === 'file:') {
            // First try a local JSON file shipped with the frontend
            try {
                const localResp = await fetch(`assets/data/hostels.json`);
                if (localResp.ok) return localResp.json();
            } catch (e) {
                // ignore and use embedded fallback
            }
            // Minimal embedded fallback so the homepage still works offline
            return [
                {
                    id: 1,
                    name: 'Lurambi Hostel',
                    slug: 'lurambi-hostel',
                    rooms_available: 20,
                    description: 'Comfortable, secure hostel near campus.',
                    images: [
                        'assets/images/hostels/lurambi-outside.jpg',
                        'assets/images/hostels/lurambi-hall.jpg',
                        'assets/images/hostels/lurambi-room.jpg'
                    ]
                },
                {
                    id: 2,
                    name: 'Sichirai Hostel',
                    slug: 'sichirai-hostel',
                    rooms_available: 18,
                    description: 'Affordable rooms with great community.',
                    images: [
                        'assets/images/hostels/sichirai-outside.jpg',
                        'assets/images/hostels/sichirai-hall.jpg',
                        'assets/images/hostels/sichirai-room.jpg'
                    ]
                },
                {
                    id: 3,
                    name: 'Kefinco Hostel',
                    slug: 'kefinco-hostel',
                    rooms_available: 15,
                    description: 'Well-located with good amenities.',
                    images: [
                        'assets/images/hostels/kefinco-outside.jpg',
                        'assets/images/hostels/kefinco-hall.jpg',
                        'assets/images/hostels/kefinco-room.jpg'
                    ]
                }
            ];
        }
        const response = await fetch(`${API_BASE_URL}/hostels/${params}`);
        if (!response.ok) throw new Error('Failed to fetch hostels');
        return response.json();
    },
    async getHostel(id) {
        if (location.protocol === 'file:') {
            // Try to load a per-hostel local JSON if present
            try {
                const localResp = await fetch(`assets/data/hostels/${id}.json`);
                if (localResp.ok) return localResp.json();
            } catch (e) {}
            // Otherwise, search the embedded list from getHostels()
            const list = await this.getHostels();
            return list.find(h => String(h.id) === String(id)) || list.find(h => h.slug === String(id)) || null;
        }
        const response = await fetch(`${API_BASE_URL}/hostels/${id}/`);
        if (!response.ok) throw new Error('Hostel not found');
        return response.json();
    },
    async updateHostel(id, data) {
        return this.authFetch(`/hostels/${id}/`, {
            method: 'PATCH',
            body: JSON.stringify(data),
        });
    },
    // Bookings
    async getBookings() { return this.authFetch('/bookings/'); },
    async getBooking(id) { return this.authFetch(`/bookings/${id}/`); },
    async createBooking(data) { return this.authFetch('/bookings/', { method: 'POST', body: JSON.stringify(data) }); },
    async updateBooking(id, data) { return this.authFetch(`/bookings/${id}/`, { method: 'PATCH', body: JSON.stringify(data) }); },
    // Payments
    async getPayments() { return this.authFetch('/payments/'); },
    async createPayment(data) { return this.authFetch('/payments/', { method: 'POST', body: JSON.stringify(data) }); },
    async initiateStkPush(bookingId, phoneNumber = '') {
        return this.authFetch('/payments/stk-push/', {
            method: 'POST',
            body: JSON.stringify({ booking: bookingId, phone_number: phoneNumber }),
        });
    },
    async completeMockStkPayment(paymentId) {
        return this.authFetch(`/payments/${paymentId}/mock-complete/`, { method: 'POST' });
    },
    // Complaints
    async getComplaints() { return this.authFetch('/complaints/'); },
    async createComplaint(data) { return this.authFetch('/complaints/', { method: 'POST', body: JSON.stringify(data) }); },
    // Maintenance
    async getMaintenance() { return this.authFetch('/maintenance/'); },
    async createMaintenance(data) { return this.authFetch('/maintenance/', { method: 'POST', body: JSON.stringify(data) }); },
    // Announcements (public)
    async getAnnouncements() {
        if (location.protocol === 'file:') {
            try {
                const localResp = await fetch('assets/data/announcements.json');
                if (localResp.ok) return localResp.json();
            } catch (e) {}
            return [];
        }
        const response = await fetch(`${API_BASE_URL}/announcements/`);
        if (!response.ok) throw new Error('Failed to fetch announcements');
        return response.json();
    },
    // Admin endpoints
    async adminGetStats() { return this.authFetch('/reports/dashboard/'); },
    // New: get all users (admin only) – you must implement this endpoint in accounts
    async adminGetUsers() { return this.authFetch('/auth/users/'); },
};