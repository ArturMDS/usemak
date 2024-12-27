
window.onload = function() {
    document.getElementById('loader-wrapper').style.display = 'none';
    document.getElementById('content').style.display = 'block';
};

function loading() {
    document.getElementById('loader-wrapper').style.display = 'flex';
    document.getElementById('content').style.display = 'none';
};

