var checkbox1 = document.querySelector("input[id=id_payment_options_0]");
var checkbox2 = document.querySelector("input[id=id_payment_options_1]");

checkbox1.addEventListener('change', function() {
if (this.checked) {
    document.querySelector("div[id=details]").style.display = 'none';
    document.querySelector("input[id=id_payment_options_1]").checked = false;
} else {
    document.querySelector("div[id=details]").style.display = '';
    document.querySelector("input[id=id_payment_options_1]").checked = true;
}
});

checkbox2.addEventListener('change', function() {
    if (this.checked) {
        checkbox1.checked = false;
        document.querySelector("div[id=details]").style.display = '';
    }
});