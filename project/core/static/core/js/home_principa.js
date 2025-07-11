
document.addEventListener("DOMContentLoaded", function () {
  // === EFECTO NAVBAR AL HACER SCROLL ===
    window.addEventListener("scroll", function () {
        const navbar = document.getElementById("navbar");
        if (navbar && window.scrollY > 100) {
            navbar.classList.add("navbar-scrolled");
        } else if (navbar) {
            navbar.classList.remove("navbar-scrolled");
        }
    });

  // === AUTOPLAY VIDEO SCROLL ===
    const video = document.getElementById("video-principal");
    if (video) {
        const videoObserver = new IntersectionObserver(
            (entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        video.play().catch(console.log);
                    } else {
                        video.pause();
                    }
                });
            },
            { threshold: 0.5 }
        );
        videoObserver.observe(video);
    }

  // === ANIMACIONES DE APARICIÓN ===
    const revealElements = document.querySelectorAll(".mostrar-al-desplazar");
    const revealObserver = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("visible");
                }
            });
        },
        { threshold: 0.2 }
    );
    revealElements.forEach((element) => revealObserver.observe(element));

  // === BOTÓN DESPLAZAMIENTO SUAVE ===
    const botones = document.querySelectorAll(
        ".boton-video, .indicador-desplazamiento"
    );
    botones.forEach((button) => {
        button.addEventListener("click", function (e) {
            const href = this.getAttribute("href");
            if (href && href.startsWith("#")) {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: "smooth" });
                }
            }
        });
    });

  // === PARALLAX SOLO EN ESCRITORIO ===
    function isDesktop() {
        return window.innerWidth > 768;
    }

    if (isDesktop()) {
        window.addEventListener("scroll", function () {
            const scrolled = window.pageYOffset;
            const seccionPrincipal = document.querySelector(".seccion-principal");
            const seccionConFondo = document.querySelector(".seccion-con-fondo");
            
            if (seccionPrincipal) {
        seccionPrincipal.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
        if (seccionConFondo) {
            const sectionScrolled = scrolled - seccionConFondo.offsetTop;
            if (sectionScrolled > 0) {
                seccionConFondo.style.backgroundPositionY = `${
                    sectionScrolled * 0.3}px`;
                }
            }
        });
    }

  // === MENÚ HAMBURGUESA ===
    const toggle = document.getElementById("toggle-menu");
    const menu = document.querySelector(".menu-principal");
    
    if (toggle && menu) {
        toggle.addEventListener("click", () => {
            menu.classList.toggle("abierto");
        });
    }

  // === SUBMENÚS EN MÓVILES ===
  // === SUBMENÚS EN MÓVILES CON EXCLUSIVIDAD ===
    const submenuItems = document.querySelectorAll(".menu-desplegable");
    submenuItems.forEach((item) => {
        const link = item.querySelector("a");
        const submenu = item.querySelector(".elementos-submenu");

    if (link && submenu) {
        link.addEventListener("click", function (e) {
        // Solo activar en modo móvil
        if (window.innerWidth <= 1280) {
            e.preventDefault();
            
            const isVisible = submenu.style.display === "block";
            
            document.querySelectorAll(".elementos-submenu").forEach((el) => {
                el.style.display = "none";
            }); // Cerrar todos los submenús

            submenu.style.display = isVisible ? "none" : "block";
        }
    });
}
});// Mostrar este solo si estaba oculto

  // === OPTIMIZACIÓN ===
    function throttle(func, wait) {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => {
                func(...args);
            }, wait);
        };
    }

    const optimizedScrollHandler = throttle(function () {
        console.log("Scroll optimizado ejecutado");
    }, 100);
    
    window.addEventListener("scroll", optimizedScrollHandler);

  // === REDIMENSIONAMIENTO ===
    window.addEventListener("resize", function () {
        if (window.innerWidth <= 1280) {
            const seccionPrincipal = document.querySelector(".seccion-principal");
            if (seccionPrincipal) {
                seccionPrincipal.style.transform = "none";
            }
            
            const seccionConFondo = document.querySelector(".seccion-con-fondo");
            if (seccionConFondo) {
                seccionConFondo.style.backgroundPositionY = "center";
            }
        }
    
    });

  // === PRECARGA DE IMÁGENES ===
    function preloadImages() {
        const imagesToPreload = [
            "/static/img/fondo-header.png",
            "/static/img/fogo_abajo.png",
            "/static/img/logo44.jpg",
        ];
        
        imagesToPreload.forEach((src) => {
            const img = new Image();
            img.src = src;
        });
    }preloadImages();

  // === ACCESIBILIDAD ===
    document.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
            const activeElement = document.activeElement;
            if (activeElement.classList.contains("boton-video")) {
                activeElement.click();
            }
        }
        if (e.key === "Escape") {
            document.querySelectorAll(".elementos-submenu").forEach((menu) => {
                menu.style.display = "none";
            });
        }
    });
    console.log("Agronova - Sistema inicializado correctamente");
});
