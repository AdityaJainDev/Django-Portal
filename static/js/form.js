let checkbox1 = document.querySelector("input[id=id_payment_options_0]");
let checkbox2 = document.querySelector("input[id=id_payment_options_1]");

checkbox1.addEventListener('change', function() {
if (this.checked) {
    document.querySelector("div[id=details]").style.display = 'none';
    document.querySelector("input[id=id_payment_options_1]").checked = false;
    document.querySelector("div[id=mandate]").style.display = 'none';
    document.querySelector("div[id=confirm]").style.display = 'none';
    document.querySelector("input[id=id_confirm]").required = false;
} else {
    document.querySelector("div[id=details]").style.display = '';
    document.querySelector("input[id=id_payment_options_1]").checked = true;
    document.querySelector("div[id=mandate]").style.display = '';
    document.querySelector("div[id=confirm]").style.display = '';
}
});


checkbox2.addEventListener('change', function() {
    if (this.checked) {
        checkbox1.checked = false;
        document.querySelector("div[id=details]").style.display = '';
        document.querySelector("div[id=mandate]").style.display = '';
        document.querySelector("div[id=confirm]").style.display = '';
        document.querySelector("input[id=id_confirm]").required = true;
    }
});


window.addEventListener('load', function() {
    if (checkbox2.checked) {
        document.querySelector("input[id=id_confirm]").required = true;
    } else {
        document.querySelector("input[id=id_confirm]").required = false;
    }
});

window.onload = function() {
    if (checkbox1.checked) {
        document.querySelector("input[id=id_confirm]").required = false;
        document.querySelector("div[id=details]").style.display = 'none';
        document.querySelector("input[id=id_payment_options_1]").checked = false;
        document.querySelector("div[id=mandate]").style.display = 'none';
        document.querySelector("div[id=confirm]").style.display = 'none';
    }
};