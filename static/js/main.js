window.addEventListener('load', setStartInfo);

function setStartInfo() {
    document.getElementById('changelog-egg')
        .addEventListener('click', function () {window.location.href = '/study/changelog';});
}