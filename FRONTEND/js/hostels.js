// Function to display hostel cards in a container, supports multiple images
function displayHostels(containerId, hostels) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = '';
    hostels.forEach(hostel => {
        // Get main image (first in images list) or fallback
        const images = hostel.images || [];
        const mainImage = images.length > 0 ? images[0] : (hostel.image || '../assets/images/hostel-placeholder.jpg');
        const card = document.createElement('div');
        card.className = 'hostel-card';
        card.innerHTML = `
            <div class="hostel-image-wrap">
                <img src="${mainImage}" alt="${hostel.name}" class="hostel-image" />
                <div class="mini-gallery">
                    ${[0,1,2].map(i => `<img src="${images[i] || mainImage}" alt="${hostel.name} photo ${i+1}"/>`).join('')}
                </div>
            </div>
            <div class="hostel-info">
                <h3>${hostel.name}</h3>
                <p class="hostel-location"><i class="fas fa-map-marker-alt"></i> ${hostel.location}</p>
                <p class="hostel-price">KSh ${hostel.price_per_semester} / semester</p>
                <div class="hostel-rating"><i class="fas fa-star"></i> ${hostel.rating}</div>
                <a href="hostel-details.html?id=${hostel.id}" class="btn-primary">View Details</a>
            </div>
        `;
        container.appendChild(card);
    });
}

// Fallback sample data if API is unavailable
const FALLBACK_HOSTELS = [
    {
        id: 'lurambi',
        name: 'Lurambi Hostel',
        location: 'Lurambi, Kakamega',
        price_per_semester: '12000.00',
        rating: 4.2,
        images: ['assets/images/lurambi.jpg','assets/images/lurambi.jpg','assets/images/lurambi.jpg'],
        description: 'Affordable and secure hostel located in Lurambi area, just 1 km from MMUST main gate.',
        amenities: ['Wi-Fi','Water','Electricity','Security'],
        gender: 'Mixed', rooms_available: 15, total_rooms:20
    },
    {
        id: 'sichirai',
        name: 'Sichirai Hostel',
        location: 'Sichirai, Kakamega',
        price_per_semester: '18000.00',
        rating: 4.5,
        images: ['assets/images/sichirai.jpg','assets/images/sichirai.jpg','assets/images/sichirai.jpg'],
        description: 'Modern hostel in the quiet Sichirai neighbourhood.',
        amenities: ['Wi-Fi','Water','Electricity','Security','Cafeteria'],
        gender: 'Female', rooms_available:8, total_rooms:12
    },
    {
        id: 'kefinco',
        name: 'Kefinco Hostel',
        location: 'Kefinco, Kakamega',
        price_per_semester: '10000.00',
        rating: 3.9,
        images: ['assets/images/kefinco.jpg','assets/images/kefinco.jpg','assets/images/kefinco.jpg'],
        description: 'Budget-friendly hostel located near Kefinco.',
        amenities: ['Water','Electricity','Security'],
        gender: 'Male', rooms_available:20, total_rooms:25
    }
];

// Helper used by pages to fetch hostels with graceful fallback
async function fetchHostelsWithFallback(params=''){
    try{
        const hostels = await API.getHostels(params);
        if (!hostels || hostels.length === 0) return FALLBACK_HOSTELS;
        return hostels;
    }catch(e){
        console.warn('API unavailable, using fallback hostels.', e);
        return FALLBACK_HOSTELS;
    }
}