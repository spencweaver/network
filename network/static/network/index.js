document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#newPost').addEventListener('click', () => newPost());
});

function newPost() {
    alert("newPost");
}