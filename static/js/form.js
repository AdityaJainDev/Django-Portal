var checkbox = document.querySelector("input[id=id_options_0]");

checkbox.addEventListener('change', function() {
if (this.checked) {
    document.querySelector("input[id=id_owner]").style.display = 'none';
    document.querySelector("label[for=id_owner]").style.display = 'none';

    document.querySelector("input[id=id_iban]").style.display = 'none';
    document.querySelector("label[for=id_iban]").style.display = 'none';

    document.querySelector("input[id=id_bic]").style.display = 'none';
    document.querySelector("label[for=id_bic]").style.display = 'none';

    document.querySelector("input[id=id_options_1]").checked = false;
} else {
    document.querySelector("input[id=id_owner]").style.display = '';
    document.querySelector("label[for=id_owner]").style.display = '';

    document.querySelector("input[id=id_iban]").style.display = '';
    document.querySelector("label[for=id_iban]").style.display = '';

    document.querySelector("input[id=id_bic]").style.display = '';
    document.querySelector("label[for=id_bic]").style.display = '';

    document.querySelector("input[id=id_options_1]").checked = true;
}
});