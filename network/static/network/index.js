document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#newPost').addEventListener('submit', function(event) {
        event.preventDefault();
        newPost();
    });
    // document.querySelector('#like').addEventListener('click', () => likePost);
    

    viewPosts();

    
});



function likePost(post_id) {
    fetch(`like/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            liked: true
        })
    });
    console.log("liked");
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
    .then(response => response.json())
    .then(result => {
        console.log(result);
        viewPosts();
    });
}

function viewPosts() {

    // empty the post form
    document.querySelector('.post_body').value = '';
    document.querySelector('#posts_list').innerHTML = '';

    // load the requested posts
    fetch('post_view')
    .then(response => response.json())
    .then(post => {
        // List out each post
        for (var i = 0; i < post.length; i++) {
            let body = post[i].body;
            let id = post[i].id;

            const li = document.createElement('li')
            li.innerHTML = `${post[i].id} ${post[i].author}<br> ${body}<br>${post[i].timestamp} <button onclick="likePost(${id})">Like</button>`;
            li.classList.add('post_item');
            document.querySelector('#posts_list').append(li);
        }
    });
}