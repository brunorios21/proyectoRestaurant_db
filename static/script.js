// Inicialización del carrusel con Bootstrap
document.addEventListener('DOMContentLoaded', function () {
    const carouselElement = document.querySelector('#carouselExampleIndicators');
    if (carouselElement) {
        const carousel = new bootstrap.Carousel(carouselElement, {
            interval: 3000, // Cambia de imagen cada 3 segundos
            ride: 'carousel'
        });
    }
});