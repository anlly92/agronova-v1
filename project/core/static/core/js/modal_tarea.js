function abrirModalTarea() {
    document.getElementById("modal-tarea").style.display = "block";
}

function cerrarModalTarea() {
    document.getElementById("modal-tarea").style.display = "none";
}  

function abrirModalEliminar() {
    const inputIdEliminar = document.getElementById('id_evento_eliminar');
    const modalEliminar = document.getElementById('modal-eliminar');

    if (inputIdEliminar && inputIdEliminar.value !== '') {
        modalEliminar.style.display = "block";
    } else {
        alert("Primero debes seleccionar una tarea del calendario.");
    }

}

function cerrarModalEliminar() {
    document.getElementById("modal-eliminar").style.display = "none";
}

function abrirModalActualizar() {
    const inputIdActualizar = document.getElementById('id_evento_actualizar');
    const modalActualizar = document.getElementById("modal-actualizar");

    if (inputIdActualizar && inputIdActualizar.value !== '') {
            modalActualizar.style.display = "block";
    } else {
        alert("Primero debes seleccionar una tarea del calendario.");
    }
}

function cerrarModalActualizar() {
    document.getElementById("modal-actualizar").style.display = "none";
}