
document.getElementById('numero_btn').addEventListener('click', function() {
    window.alert('Número generado y correo enviado');
    document.getElementById('action').value = 'numero';
    document.getElementById('myForm').submit();
});



// document.addEventListener('DOMContentLoaded', function() {
//     var inputs = document.querySelectorAll('input');
//     var enviarBtn = document.getElementById('enviarBtn');

//     enviarBtn.addEventListener('click', function() {
//         var passInput = document.getElementById('passInput').value;
//         var confirmedPassInput = document.getElementById('confirmedPassInput').value;
//         var formValid = true;

//         inputs.forEach(function(input) {
//             if (input.value === '') {
//                 input.classList.add('invalid');
//                 formValid = false;
//             } else {
//                 input.classList.remove('invalid');
//             }

//             input.addEventListener('input', function() {
//                 if (input.value !== '') {
//                     input.classList.remove('invalid');
//                 }
//             });
//         });

//         if (passInput !== confirmedPassInput) {
//             alert('Las contraseñas no coinciden');
//             formValid = false;
//         }

//         if (formValid) {
//             if (isPassWeak(passInput)) {
//                 alert('La contraseña es débil. Debe ser más fuerte. \n- Longitud de contraseña: como mínimo 8 caracteres\n- Caracteres numéricos: como mínimo 2 números'
//                 +'\n- Caracteres de símbolos: como mínimo 1 carácter especial\n- Letras mayúsculas: como mínimo 1 letra mayúscula\n- Letras minúsculas: como mínimo 1 letra minúscula');
//             } else {
//                 alert('Formulario enviado correctamente');
//                 document.getElementById('formRegister').submit();
//             }
//         } else {
//             alert('Por favor, completa todos los campos y verifica las contraseñas');
//         }
//     });

//     function isPassWeak(passInput) {
//         // Evalúa la fortaleza de la contraseña (criterios simples)
//         // Puedes ajustar estos criterios según tus necesidades
//         return passInput.length < 8 || !/[A-Z]/.test(passInput) || !/[a-z]/.test(passInput) || !/\d/.test(passInput) || !/[!@#$%^&*()_+\-=[\]{};':"\\|,.<>/?]+/.test(passInput);
//     }

//     var phoneInput = document.getElementById('phoneInput');

//     phoneInput.addEventListener('input', function() {
//         phoneInput.value = phoneInput.value.replace(/\D/g, '').slice(0, 10);
//     });
    
// });