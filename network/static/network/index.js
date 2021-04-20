document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#newPost').addEventListener('submit', function(event) {
        // event.preventDefault();
        newPost();
    });
    document.querySelectorAll('.edit_button').forEach(button => {
        button.onclick = () => {
            editPost(button.dataset.post);
        };
    });
    // document.querySelector('#like').addEventListener('click', () => likePost);
    

    // viewPosts(); 
});


function editPost(post_id) {
    fetch(`/edit/${post_id}`)
    .then(response => response.json())
    .then(post => {
        console.log(post);
        body = post.body;
        console.log(body);
        document.querySelector('#post_edit_text').value = body;
    })
}



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
    // document.querySelector('#posts_list').innerHTML = '';
    
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
        // viewPosts();
    });
}

function viewPosts() {

    // empty the post form
    document.querySelector('.post_body').value = '';

    // load the requested posts
    fetch('post_view')
    .then(response => response.json())
    .then(post => {
        // List out each post
        for (var i = 0; i < post.length; i++) {
            let body = post[i].body;
            let id = post[i].id;

            const li = document.createElement('li')
            li.innerHTML = `${post[i].id} ${post[i].author}<br> ${body}<br>${post[i].timestamp} <button onclick="likePost(${id})">Like</button><button onclick="editPost(${id})">Edit</button>`;
            li.classList.add('post_item');
            li.id = `post_item_${id}`;
            document.querySelector('#posts_list').append(li);
        }
    });
}