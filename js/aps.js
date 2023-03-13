// ==================================================== typing ainimation ==================================================== //
var typed = new Typed(".text-typing", {
    strings: [" ", "Web Designer", "web Devoloper", "Graphic Designer", "YouTuber"],
    typeSpeed: 100,
    BackSpeed: 60,
    loop: true
});

// ==================================================== navbar ainimation ==================================================== //

// ==================================================== menu js  ==================================================== //

let barsIcon = document.querySelector('#menu_bars');
let barsClos = document.querySelector('#menu_clos');
let bodyBox = document.querySelector('body');
let cllosMenuBox = document.querySelector('.cllos_menu_box');

var mediaQuery = window.matchMedia("(min-width: 1200px)");

// medya sorgusu durumunu dinle
mediaQuery.addListener(function() {
    if (mediaQuery.matches) {
        bodyBox.classList.remove('active');
    }
});

barsIcon.addEventListener('click', function() {
    bodyBox.classList.add('active')
});
barsClos.addEventListener('click', function() {
    bodyBox.classList.remove('active')
});

cllosMenuBox.addEventListener('click', function() {
        if (bodyBox.classList.contains('active')) bodyBox.classList.remove('active');
    })
    // ==================================================== menu js  ==================================================== //


let Alink = document.querySelectorAll('.btn-link');
var optionSection = document.querySelectorAll('section');

Alink.forEach(links => {
    links.addEventListener('click', function() {
        closeLinks()
        links.classList.add('active');
        let atrLink = links.getAttribute("data-a");

        optionSection.forEach(elementSection => {
            let atrSection = elementSection.getAttribute("data-section");
            if (atrLink === atrSection) {
                cleaning();
                elementSection.classList.add('hidden-active')
            }

        });
    })
});

// ====================================================  modal js start ==================================================== //

let modalBox = document.querySelector('.portfolio_modal_box');
let modalBtn = document.querySelectorAll('.portfolio_btn');
let coloseIcon = document.querySelector('#icon_X');
modalBtn.forEach(btnItems => {
    btnItems.addEventListener('click', function() {
        modalBox.classList.add('active');
    })
});
coloseIcon.addEventListener('click', function() {
    modalBox.classList.add('closing');
    setTimeout(function() {
        modalBox.classList.remove('active');
        modalBox.classList.remove('closing');
    }, 1400); // 0.4s + 1s delay = 1.4s = 1400ms
});


let scrollsection = document.querySelectorAll('.section');
console.log(scrollsection)
let scrollHeight = Math.max(
    document.body.scrollHeight, document.documentElement.scrollHeight,
    document.body.offsetHeight, document.documentElement.offsetHeight,
    document.body.clientHeight, document.documentElement.clientHeight
);

// "a" to remove an active class
function closeLinks() {
    Alink.forEach(closeLink => {
        closeLink.classList.remove('active')
    });
};
// "section" to remover an active class
function cleaning() {
    optionSection.forEach(closed => {
        closed.classList.remove('hidden-active');
    });
}
// ==================================================== section ainimation ==================================================== //