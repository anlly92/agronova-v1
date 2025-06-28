// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    
    // === EFECTO NAVBAR AL HACER SCROLL ===
            // Navbar scroll effect
        window.addEventListener('scroll', function() {
            const navbar = document.getElementById('navbar');
            if (window.scrollY > 100) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });
    
    window.addEventListener('scroll', function() {
        // Removido el efecto de cambio por scroll ya que ahora la navbar es siempre estática
        // La navbar mantiene su estado fijo con hover
    });

    // === AUTOPLAY DE VIDEO AL HACER SCROLL ===
    const video = document.getElementById('video-principal');
    
    // Configuración del Intersection Observer para el video
    const videoObserverOptions = {
        root: null, // viewport
        rootMargin: '0px',
        threshold: 0.5 // Se activa cuando el 50% del video está visible
    };
    
    const videoObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // El video está visible, reproducir
                video.play().catch(error => {
                    console.log('Error al reproducir automáticamente:', error);
                    // Algunos navegadores bloquean autoplay, esto es normal
                });
            } else {
                // El video no está visible, pausar
                if (!video.paused) {
                    video.pause();
                }
            }
        });
    }, videoObserverOptions);
    
    // Comenzar a observar el video
    if (video) {
        videoObserver.observe(video);
    }

    // === ANIMACIONES DE REVEAL PARA LAS SECCIONES DE CONTENIDO ===
    const revealElements = document.querySelectorAll('.mostrar-al-desplazar');
    
    const revealObserverOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.2 // Se activa cuando el 20% del elemento está visible
    };
    
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, revealObserverOptions);

    // Observar todos los elementos que deben revelarse
    revealElements.forEach(element => {
        revealObserver.observe(element);
    });

    // === SMOOTH SCROLL PARA EL BOTÓN CTA ===
    const boton = document.querySelectorAll('.boton-video');
    
    boton.forEach(button => {
        button.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Solo aplicar smooth scroll si es un enlace interno (comienza con #)
            if (href && href.startsWith('#')) {
                e.preventDefault();
                
                const targetElement = document.querySelector(href);
                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // === EFECTO PARALLAX MEJORADO (Opcional - para dispositivos de escritorio) ===
    function isDesktop() {
        return window.innerWidth > 768;
    }
    
    if (isDesktop()) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const seccionPrincipal = document.querySelector('.seccion-principal');
            const seccionConFondo = document.querySelector('.seccion-con-fondo');
            
            if (seccionPrincipal) {
                // Efecto parallax para la sección hero
                seccionPrincipal.style.transform = `translateY(${scrolled * 0.5}px)`;
            }
            
            if (seccionConFondo) {
                // Efecto parallax para la sección con fondo
                const sectionTop = seccionConFondo.offsetTop;
                const sectionScrolled = scrolled - sectionTop;
                
                if (sectionScrolled > 0) {
                    seccionConFondo.style.backgroundPositionY = `${sectionScrolled * 0.3}px`;
                }
            }
        });
    }

    // === MANEJO DE MENÚS DESPLEGABLES EN MÓVIL ===
    const submenuItems = document.querySelectorAll('.menu-desplegable');
    
    submenuItems.forEach(item => {
        const link = item.querySelector('a');
        const submenu = item.querySelector('.elementos-submenu');
        
        if (window.innerWidth <= 768) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                
                // Toggle del menú desplegable
                if (submenu.style.display === 'block') {
                    submenu.style.display = 'none';
                } else {
                    // Cerrar otros menús abiertos
                    document.querySelectorAll('.elementos-submenu').forEach(menu => {
                        menu.style.display = 'none';
                    });
                    
                    submenu.style.display = 'block';
                }
            });
        }
    });

    // === OPTIMIZACIÓN DE PERFORMANCE ===
    // Throttle function para optimizar eventos de scroll
    function throttle(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Aplicar throttle al evento de scroll si hay muchos elementos
    const optimizedScrollHandler = throttle(function() {
        // Aquí puedes agregar más funcionalidades de scroll si es necesario
        console.log('Scroll optimizado ejecutado');
    }, 100);

    window.addEventListener('scroll', optimizedScrollHandler);

    // === MANEJO DE REDIMENSIONAMIENTO DE VENTANA ===
    window.addEventListener('resize', function() {
        // Reconfigurar efectos basados en el tamaño de pantalla
        if (window.innerWidth <= 768) {
            // Desactivar efectos parallax en móvil
            const seccionPrincipal = document.querySelector('.seccion-principal');
            if (seccionPrincipal) {
                seccionPrincipal.style.transform = 'none';
            }
            
            const seccionConFondo = document.querySelector('.seccion-con-fondo');
            if (seccionConFondo) {
                seccionConFondo.style.backgroundPositionY = 'center';
            }
        }
    });

    // === PRECARGA DE IMÁGENES IMPORTANTES ===
    function preloadImages() {
        const imagesToPreload = [
            '/static/principal_app/img/header.jpg',
            '/static/principal_app/img/fogo_abajo.png',
            '/static/principal_app/img/logo44.jpg'
        ];
        
        imagesToPreload.forEach(src => {
            const img = new Image();
            img.src = src;
        });
    }
    
    // Ejecutar precarga
    preloadImages();

    // === ACCESIBILIDAD: NAVEGACIÓN POR TECLADO ===
    document.addEventListener('keydown', function(e) {
        // Manejar navegación con Enter en elementos clickeables
        if (e.key === 'Enter') {
            const activeElement = document.activeElement;
            
            if (activeElement.classList.contains('boton-video')) {
                activeElement.click();
            }
        }
        
        // Cerrar menús desplegables con Escape
        if (e.key === 'Escape') {
            document.querySelectorAll('.elementos-submenu').forEach(menu => {
                menu.style.display = 'none';
            });
        }
    });

    // === LOG DE INICIALIZACIÓN ===
    console.log('🌱 Agronova - Sistema inicializado correctamente');
    console.log('✅ Efectos de scroll activados');
});