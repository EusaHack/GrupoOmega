document.querySelectorAll('.cont-int').forEach(container => {
    const colorInput = container.querySelector('.color-picker'),
    textArea = container.querySelector('textarea'),
    button = container.querySelector('.color-button'),
    hex = document.querySelector('#hex');

    colorInput.addEventListener('input', () => {
        let color = colorInput.value;
        hex.style.color = color;
        hex.innerHTML = color;
        textArea.style.color = color;
        button.style.backgroundColor = color;
    });
});


document.querySelectorAll('.cont-int').forEach(container => {
    const colorInput = container.querySelector('.color-picker-2'),
    button = container.querySelector('.color-button1'),
    hex = document.querySelector('#hex1');

    colorInput.addEventListener('input', () => {
        let color = colorInput.value;
        hex.style.color = color;
        hex.innerHTML = color;
        button.style.backgroundColor = color;
    });
});