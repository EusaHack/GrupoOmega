document.getElementById('number_btn').addEventListener('click', function() {
    document.getElementById('action').value = 'numero';
    document.getElementById('myForm').submit();
});

function openModalReset() {
    document.getElementById('modal-reset').style.display = 'block';
}

function closeModalReset() {
    document.getElementById('modal-reset').style.display = 'none';
}

const linkPassword = document.querySelector('.link-password a');
linkPassword.addEventListener('click', openModalReset);
