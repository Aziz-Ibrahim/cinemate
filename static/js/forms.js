/**
 * Toggles the visibility of a password input field.
 *
 * @param {HTMLInputElement} input - The password input element.
 * @param {HTMLElement} toggle - The icon element that triggers the toggle.
 */
function togglePasswordVisibility(input, toggle) {
    if (input.type === 'password') {
        input.type = 'text';
        toggle.classList.remove('fa-eye');
        toggle.classList.add('fa-eye-slash');
    } else {
        input.type = 'password';
        toggle.classList.remove('fa-eye-slash');
        toggle.classList.add('fa-eye');
    }
}

/**
 * Adds password toggle functionality to password input fields.
 */
function addPasswordToggles() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');

    passwordInputs.forEach(input => {
        const inputGroup = document.createElement('div');
        inputGroup.classList.add('input-group');

        const inputWrapper = document.createElement('div');
        inputWrapper.style.flexGrow = '1';
        input.parentNode.insertBefore(inputGroup, input);
        inputGroup.appendChild(inputWrapper);
        inputWrapper.appendChild(input);

        const inputGroupAppend = document.createElement('div');
        inputGroupAppend.classList.add('input-group-append');

        const inputGroupText = document.createElement('span');
        inputGroupText.classList.add('input-group-text');
        inputGroupText.style.display = 'flex';
        inputGroupText.style.alignItems = 'center';
        inputGroupText.style.height = '38px'; // Set height to match Bootstrap input

        const toggleIcon = document.createElement('i');
        toggleIcon.classList.add('fa', 'fa-eye');
        toggleIcon.id = input.id + '-toggle';

        inputGroupAppend.appendChild(inputGroupText);
        inputGroupText.appendChild(toggleIcon);
        inputGroup.appendChild(inputGroupAppend);

        toggleIcon.addEventListener('click', function() {
            togglePasswordVisibility(input, toggleIcon);
        });
    });
}

document.addEventListener('DOMContentLoaded', function() {
    addPasswordToggles();
});