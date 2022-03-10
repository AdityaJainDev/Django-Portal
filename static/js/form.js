var checkbox1 = document.querySelector("input[id=id_options_0]");
var checkbox2 = document.querySelector("input[id=id_options_1]");

checkbox1.addEventListener('change', function() {
if (this.checked) {
    document.querySelector("input[id=id_owner]").style.display = 'none';
    document.querySelector("input[id=id_owner]").required = false;
    document.querySelector("label[for=id_owner]").style.display = 'none';

    document.querySelector("input[id=id_iban]").style.display = 'none';
    document.querySelector("input[id=id_iban]").required = false;
    document.querySelector("label[for=id_iban]").style.display = 'none';

    document.querySelector("input[id=id_bic]").style.display = 'none';
    document.querySelector("input[id=id_bic]").required = false;
    document.querySelector("label[for=id_bic]").style.display = 'none';

    document.querySelector("input[id=id_options_1]").checked = false;
} else {
    document.querySelector("input[id=id_owner]").style.display = '';
    document.querySelector("input[id=id_owner]").required = true;
    document.querySelector("label[for=id_owner]").style.display = '';

    document.querySelector("input[id=id_iban]").style.display = '';
    document.querySelector("input[id=id_iban]").required = true
    document.querySelector("label[for=id_iban]").style.display = '';

    document.querySelector("input[id=id_bic]").style.display = '';
    document.querySelector("input[id=id_bic]").required = true;
    document.querySelector("label[for=id_bic]").style.display = '';

    document.querySelector("input[id=id_options_1]").checked = true;
}
});

checkbox2.addEventListener('change', function() {
    if (this.checked) {
        checkbox1.checked = false;
        document.querySelector("input[id=id_owner]").style.display = '';
        document.querySelector("input[id=id_owner]").required = true;
        document.querySelector("label[for=id_owner]").style.display = '';

        document.querySelector("input[id=id_iban]").style.display = '';
        document.querySelector("input[id=id_iban]").required = true
        document.querySelector("label[for=id_iban]").style.display = '';

        document.querySelector("input[id=id_bic]").style.display = '';
        document.querySelector("input[id=id_bic]").required = true;
        document.querySelector("label[for=id_bic]").style.display = '';
    }
});