import setDarkThemeToggler from "./dark-theme.js";

window.addEventListener('load', setStartInfo);

function setStartInfo() {
    setDarkThemeToggler();

    document.getElementById('changelog-egg')
        .addEventListener('click', function () {window.location.href = '/study/changelog';});
}