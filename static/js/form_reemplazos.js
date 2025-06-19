document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('formulario');

    // Profesión: mostrar campo extra si elige "Otros"
    const profesionSelect = document.getElementById('id_profesion');
    const otraProfesionGroup = document.getElementById('otra-profesion-group');
    const otraProfesionInput = document.getElementById('id_otra_profesion');

    if (form && profesionSelect && otraProfesionGroup && otraProfesionInput) {
        function checkProfesionOption() {
            if (profesionSelect.value === 'Otros') {
                otraProfesionGroup.style.display = 'block';
                otraProfesionInput.disabled = false;
            } else {
                otraProfesionGroup.style.display = 'none';
                otraProfesionInput.value = '';
                otraProfesionInput.disabled = true;
            }
        }

        profesionSelect.addEventListener('change', checkProfesionOption);
        checkProfesionOption();
    }









    // Género: mostrar campo extra si elige "Otros"
    const generoSelect = document.getElementById('id_genero');
    const otroGeneroContainer = document.getElementById('otro-genero-container');
    const otroGeneroInput = document.getElementById('id_otro_genero');
    if (generoSelect && otroGeneroContainer && otroGeneroInput) {
        function toggleOtroGenero() {
            if (generoSelect.value === 'Otros') {
                otroGeneroContainer.style.display = 'block';
            } else {
                otroGeneroContainer.style.display = 'none';
                otroGeneroInput.value = '';
            }
        }
        generoSelect.addEventListener('change', toggleOtroGenero);
        toggleOtroGenero();
    }

    // Donde trabajar: mostrar campo extra si selecciona "Otros"
    const checkboxes = document.querySelectorAll('input[name="donde_trabajar"]');
    const otroLugarContainer = document.getElementById('otro-lugar-container');
    const otroLugarInput = document.getElementById('id_otro_lugar');
    if (checkboxes.length && otroLugarContainer && otroLugarInput) {
        function toggleOtroLugar() {
            let mostrar = false;
            checkboxes.forEach(function (checkbox) {
                if (checkbox.value === "Otros" && checkbox.checked) {
                    mostrar = true;
                }
            });
            if (mostrar) {
                otroLugarContainer.style.display = "block";
            } else {
                otroLugarContainer.style.display = "none";
                otroLugarInput.value = "";
            }
        }

        checkboxes.forEach(function (checkbox) {
            checkbox.addEventListener('change', toggleOtroLugar);
        });

        toggleOtroLugar();
    }



    if (form) {
        form.addEventListener('submit', function () {
            // Habilitar otra_profesion si corresponde
            if (typeof profesionSelect !== 'undefined' &&
                profesionSelect?.value === 'Otros' &&
                otraProfesionInput) {
                otraProfesionInput.disabled = false;
            }

            // Habilitar otro_genero si corresponde
            if (typeof generoSelect !== 'undefined' &&
                generoSelect?.value === 'Otros' &&
                otroGeneroInput) {
                otroGeneroInput.disabled = false;
            }

            // Habilitar otro_lugar si corresponde
            if (checkboxes.length && otroLugarInput) {
                const otrosSeleccionados = Array.from(checkboxes).some(checkbox =>
                    checkbox.value === "Otros" && checkbox.checked
                );
                if (otrosSeleccionados) {
                    otroLugarInput.disabled = false;
                }
            }
        });
    }

    const selectProfesionEspecialista = document.getElementById('id_profesion');
    const contenedorEunacom = document.getElementById('campo_eunacom');

    function mostrarCampoEunacomSiEsMedico() {
        if (!selectProfesionEspecialista || !contenedorEunacom) return;

        const profesionSeleccionada = selectProfesionEspecialista.value.toLowerCase();

        if (profesionSeleccionada.includes('médico')) {
            contenedorEunacom.style.display = 'block';
        } else {
            contenedorEunacom.style.display = 'none';
            const archivoEunacom = document.getElementById('id_certificado_eunacom');
            if (archivoEunacom) archivoEunacom.value = '';
        }
    }

    if (selectProfesionEspecialista && contenedorEunacom) {
        selectProfesionEspecialista.addEventListener('change', mostrarCampoEunacomSiEsMedico);
        mostrarCampoEunacomSiEsMedico();  // Ejecutar al cargar
    }



    // Modal de mensajes
    const mensajeModal = document.getElementById('mensajeModal');
    if (mensajeModal) {
        const modal = new bootstrap.Modal(mensajeModal);
        modal.show();
    }

















});




