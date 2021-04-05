document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#newPost').addEventListener('submit', () => newPost());
    // document.querySelector('#like').addEventListener('click', () => likePost);
    

    viewPosts();

    
});



function likePost() {
    fetch('like', {
        method: 'PUT',
        body: JSON.stringify({
            liked: true
        })
    });
    alert("liked");
}

function newPost() {
    // Submit Post
    body = document.querySelector('.post_body').value;
    fetch('/posts', {
        method: 'POST',
        body: JSON.stringify({
            body: body,
        })
    })
}

function viewPosts() {
    fetch('post_view')
    .then(response => response.json())
    .then(post => {
        console.log(post);

        // List out each post
        for (var i = 0; i < post.length; i++) {
            let body = post[i].body;

            const li = document.createElement('li')
            li.innerHTML = `${post[i].id} ${post[i].author}<br> ${body}<br>${post[i].timestamp} <button onclick="likePost()">Like</button>`;
            li.classList.add('post_item');
            document.querySelector('#posts_list').append(li);
        }
    });
}