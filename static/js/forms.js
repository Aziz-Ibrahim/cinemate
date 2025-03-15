function togglePassword(id) {
    var field = document.getElementById(id);
    field.type = field.type === "password" ? "text" : "password";
}