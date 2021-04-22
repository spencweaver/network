document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#newPost').addEventListener('submit', function(event) {
        newPost();
    });
    document.querySelectorAll('.edit_button').forEach(button => {
        button.onclick = () => {
            editPost(button.dataset.post);
        }
    });
    document.querySelectorAll('.like_button').forEach(button => {
        button.onclick = () => {
            likePost(button.dataset.post);
        }
    });    
});


async function likePost(post_id) {
    const fetcher = await fetch(`like/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            liked: true
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result);
        document.querySelector(`.like_counter_${post_id}`).innerHTML = `Likes: ${result.likes_count}`
    });
}


function saveEdit(post_id) {
    const post = document.querySelector(`.edit_button_${post_id} > textarea`);
    fetch(`/edit/${post_id}`, {
        method: 'POST',
        body: JSON.stringify({
            body_edit: post.value
        })
    })
    .then(response => response.json())
    .then(result => {
        console.log(result.body);
        document.querySelector(`.edit_button_${post_id}`).innerHTML = `<p>${result.body}</p>`;
    })
}


function editPost(post_id) {
    fetch(`/edit/${post_id}`)
    .then(response => response.json())
    .then(post => {
        console.log(post);
        const body = post.body;
        console.log(body);
        const form = `<textarea>${body}</textarea id="post_edit_${post_id}"><button onClick="saveEdit(${post_id})">Save</button>`;
        document.querySelector(`.edit_button_${post_id}`).innerHTML = form;
    })
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
    });
}
