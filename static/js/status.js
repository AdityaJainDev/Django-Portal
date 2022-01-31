document.addEventListener("DOMContentLoaded", function() {

    // smooth scrolling for events
    var groups = document.querySelectorAll(".group");
    for (var i=0; i < groups.length; i++) {
        groups[i].addEventListener("click", function(e) {
            if (e.target.getAttribute("data-id") != null) {
                id = e.target.getAttribute("data-id");
                target = document.querySelector(".event[data-id='" + id + "']");
                target.scrollIntoView({"behavior": "smooth"});
            } else {
                this.classList.toggle("active");
            }
        });
    }

    var tooltips = document.querySelectorAll(".tooltip");
    for (var i=0; i < tooltips.length; i++) {
        groups[i].addEventListener("click", function(e) {
            if (e.target.getAttribute("data-id") != null) {
                id = e.target.getAttribute("data-id");
                target = document.querySelector(".event[data-id='" + id + "']");
                target.scrollIntoView({"behavior": "smooth"});
            }
            e.preventDefault();
        });
    }

    // menu interactions
    accountIcon = document.querySelector("header .account .icon");
    accountOverlay = document.querySelector("header .account .overlay");
    accountIcon.addEventListener("mouseenter", function(e) {
        accountIcon.classList.add("active");
        accountOverlay.classList.add("visible");
        feedIcon.classList.remove("active");
        feedOverlay.classList.remove("visible");
    });
    accountOverlay.addEventListener("mouseleave", function(e) {
        accountOverlay.classList.remove("visible");
        accountIcon.classList.remove("active");
    });

    feedIcon = document.querySelector("header .feed .icon");
    feedOverlay = document.querySelector("header .feed .overlay");
    feedIcon.addEventListener("mouseenter", function(e) {
        feedIcon.classList.add("active");
        feedOverlay.classList.add("visible");
        accountIcon.classList.remove("active");
        accountOverlay.classList.remove("visible");
    });
    feedOverlay.addEventListener("mouseleave", function(e) {
        feedOverlay.classList.remove("visible");
        feedIcon.classList.remove("active");
    });

    // email based login
    loginButton = document.querySelector("header .account button");
    loginEmail = document.querySelector("header .account input[type=honeypotEmail1]");
    loginResult = document.querySelector("header .account .result");
    honeypot = document.querySelector("header .account input[type=text]");

    loginButton.addEventListener("click", function(e) {
        if (loginEmail.value != "" && loginEmail.value.indexOf("@") > 0 && honeypot.value == '') {
            var xhr = new XMLHttpRequest();
            xhr.open("POST", "/subscriptions/login/" + loginEmail.value);
            xhr.onload = function() {
                if (xhr.status === 204) {
                    loginResult.querySelector(".success").style.display = "block";
                } else {
                    loginResult.querySelector(".error").style.display = "block";
                }
            };
            xhr.send();
        } else {
            console.log("error sending the email");
        }
    });

});