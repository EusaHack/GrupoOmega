// Espera a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Obtiene todos los enlaces dentro de la clase 'nav-links'
    const navLinks = document.querySelectorAll('.nav-links a');

    // Agrega un evento de clic a cada enlace del menú
    navLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            // Previene el comportamiento predeterminado del enlace
            event.preventDefault();

            // Elimina la clase 'clicked' de todos los enlaces
            navLinks.forEach(item => {
                item.classList.remove('clicked');
            });

            // Agrega la clase 'clicked' al enlace seleccionado
            this.classList.add('clicked');

            // Obtiene el atributo href del enlace seleccionado
            const href = this.getAttribute('href');

            // Redirige a la página correspondiente después de un breve retraso
            if (href && href !== '#') {
                setTimeout(function() {
                    window.location.href = href;
                });
            }
        });

        // Verifica si la página actual tiene el enlace y agrega la clase 'clicked'
        const currentPage = window.location.href;
        if (link.href === currentPage) {
            link.classList.add('clicked');
        }
    });
});


// Funciones para el modal

function toggleMenu() {
    const navLinks = document.getElementById('navLinks');
    if (navLinks) {
        navLinks.classList.toggle('show');
    }
}

function closeModalWindow() {
    document.getElementById('modal').style.display = 'none';
}

function openModalForm() {
    document.getElementById('modal').style.display = 'flex'; 
}


// Funciones para el carrusel
let txtBtns = [
    "txt-1", "txt-2", "txt-3", "txt-4", "txt-5", "txt-6", "txt-7"
];

let imgRollo = document.getElementById("image-carousel");

function changeImage(imageSrc) {
    imgRollo.src = imageSrc;
}

for (let i = 0; i < txtBtns.length; i++) {
    let currentBtn = document.getElementById(txtBtns[i]);
    let imageSrc = BASE_IMAGE_URL + `cardboard-box-preview-${i + 1}.png`;
    currentBtn.onpointerenter = function() {
        changeImage(imageSrc);
    };
}