// ==================================================== toggler style swittcher ==================================================== //
let styleSwitcherToggler = document.querySelector('.style-switcher-toggler');
styleSwitcherToggler.addEventListener('click', function () {
    document.querySelector('.style-switcher').classList.toggle('open');
});
// hide style switcher on scroll
window.addEventListener('scroll', function () {
    if (document.querySelector('.style-switcher').classList.contains('open')) { }
    document.querySelector('.style-switcher').classList.remove('open')
});
// ==================================================== theme colors ==================================================== //
let alternatestyles = document.querySelectorAll(".alternate-style");
function setActiveStyle(color) {
    alternatestyles.forEach(style => {
        if (color === style.getAttribute('title')) {
            style.removeAttribute('disabled');
        }
        else {
            style.setAttribute('disabled', 'true');
        }
    });
};
// ==================================================== theme light and dark mode ==================================================== //
let dayNight = document.querySelector('.day-night');
dayNight.addEventListener('click', function () {
    dayNight.querySelector("i").classList.toggle('fa-sun');
    dayNight.querySelector("i").classList.toggle('fa-moon');
    document.body.classList.toggle('dark');
})
window.addEventListener('load', function () {
    if (document.body.classList.contains('dark')) {
        dayNight.querySelector("i").classList.add('fa-sun');
    }
    else {
        dayNight.querySelector("i").classList.add('fa-moon');

    }
});
