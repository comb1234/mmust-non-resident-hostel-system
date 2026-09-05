// Authentication module – uses API to manage user auth
const Auth = {
    // Register a new student
    async register(data) {
        try {
            const user = await API.register({
                email: data.email,
                password: data.password,
                first_name: data.fullName.split(' ')[0],
                last_name: data.fullName.split(' ').slice(1).join(' '),
                registration_number: data.regNumber,
                phone: data.phone,
                gender: data.gender,
                course: data.course,
                year_of_study: data.year,
            });
            return { success: true, user };
        } catch (error) {
            try {
                const parsed = JSON.parse(error.message);
                const firstKey = Object.keys(parsed)[0];
                const message = Array.isArray(parsed[firstKey]) ? parsed[firstKey][0] : parsed[firstKey];
                return { success: false, message };
            } catch {
                return { success: false, message: error.message };
            }
        }
    },
    // Login user
    async login(email, password) {
        try {
            const user = await API.login(email, password);
            return { success: true, user, role: user.role };
        } catch (error) {
            return { success: false, message: error.message };
        }
    },
    // Logout
    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '../login.html';
    },
    // Check if user is logged in
    isLoggedIn() {
        return !!localStorage.getItem('access_token');
    },
    // Get current user from backend
    async getCurrentUser() {
        try {
            return await API.getCurrentUser();
        } catch (error) {
            return null;
        }
    }
};