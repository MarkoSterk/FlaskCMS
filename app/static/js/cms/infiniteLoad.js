// import {deletePost} from './postCRUD.js';

function postTemplate(post, formType){
    let img=''
    if(post.coverImage){
        img=`<img src="static/images/${formType}/${post.coverImage}" class="card-img-top" style="max-height: 300px;" alt="post cover">`
    }
    if(post.images && !post.coverImage){
        img=`<img src="static/images/${formType}/${post.images[0]}" class="card-img-top" style="max-height: 300px;" alt="post cover">`
    }
    let inactive = '';
    if(post.active==false){
        inactive=`<p class="text-muted d-inline small">Inactive</p>`
    }
    
    let markup = '';

    if(formType==='posts'){
        markup = `
        <div class="col-xl-4 col-sm-12 p-2" id="card_${post._id }">
            <div class="card card-common">
                <p class="small text-secondary mt-2 ml-2 postDate">${post._createdAt}</p>
                ${img}
                <div class="card-body">
                    <h5 class="card-title">
                    ${post.title.slice(0,100)}
                    ${inactive}
                    </h5>
                    <p class="card-text">${post.text.slice(0,200)}</p>
                    <p class="small text-secondary">${post.category.join(', ')}</p>
                    <a href="/cms/post/${post._id}" class="btn btn-primary btn-sm"><i class="fas fa-edit mr-2"></i>Edit</a>
                    <a class="btn btn-danger text-light deleteBtn btn-sm" data-item-id=${post._id} data-resource="posts" data-toggle="modal" data-target="#deleteItemModal"><i class="fas fa-trash mr-2"></i>Delete</a>
                </div>
            </div>
        </div>`
    }
    else if(formType==='publications'){
        markup = `
        <div class="col-xl-4 col-sm-12 p-2" id="card_${post._id}">
            <div class="card card-common">
                <p class="small text-secondary mt-2 ml-2 postDate">${post._createdAt}</p>
                ${img}
                <div class="card-body">
                    <h5 class="card-title">
                    ${post.title.slice(0,100)}
                    ${inactive}
                    </h5>
                    <p class="card-text">${post.text.slice(0,200)}</p>
                    <p class="small text-secondary">${post.journal}</p>
                    <p class="small text-secondary">${post.doi}</p>
                    <a href="/cms/publication/${post._id}" class="btn btn-primary btn-sm"><i class="fas fa-edit mr-2"></i>Edit</a>
                    <a class="btn btn-danger text-light deleteBtn btn-sm" data-item-id=${post._id} data-resource="publications" data-toggle="modal" data-target="#deleteItemModal"><i class="fas fa-trash mr-2"></i>Delete</a>
                </div>
            </div>
        </div>`
    }
    else if(formType==='galleries'){
        markup=`<div class="col-xl-4 col-sm-12 p-2" id="card_${post._id}">
            <div class="card card-common">
            <p class="small text-secondary mt-2 ml-2 postDate">${post._createdAt}</p>
            ${img}
            <div class="card-body">
                <h5 class="card-title">
                ${post.title.slice(0,100)}
                ${inactive}
                </h5>
                <p class="card-text">${post.text.slice(0,200)}</p>
                <a href="/cms/galleries/${post._id}" class="btn btn-primary btn-sm"><i class="fas fa-edit mr-2"></i>Edit</a>
                <a class="btn btn-danger text-light btn-sm deleteBtn" data-item-id=${post._id } data-resource="galleries" data-toggle="modal" data-target="#deleteItemModal"><i class="fas fa-trash mr-2"></i>Delete</a>
            </div>
            </div>
        </div>`
    }
    else if(formType==='products'){
        markup=`<div class="col-xl-4 col-sm-12 p-2" id="card_${post._id}">
        <div class="card card-common">
          <p class="small text-secondary mt-2 ml-2 postDate">${post._createdAt}</p>
          ${img}
          <div class="card-body">
            <h5 class="card-title">
              ${post.name.slice(0,100)}
              ${inactive}
            </h5>
            <p class="card-text">${post.text.slice(0,200)}</p>
            <a href="/cms/product/${post._id}" class="btn btn-primary btn-sm"><i class="fas fa-edit mr-2"></i>Edit</a>
            <a class="btn btn-danger text-light btn-sm deleteBtn" data-item-id=${post._id} data-resource="products" data-toggle="modal" data-target="#deleteItemModal"><i class="fas fa-trash mr-2"></i>Delete</a>
          </div>
        </div>
      </div>`
    }
    else{
        markup = `
        <div class="col-xl-4 col-sm-12 p-2" id="card_${post._id}">
            <div class="card card-common">
                <p class="small text-secondary mt-2 ml-2 postDate">${post._createdAt}</p>
                ${img}
                <div class="card-body">
                    <h5 class="card-title">
                    ${post.title.slice(0,100)}
                    </h5>
                    <h5 class="card-title">
                    ${post.titleSlo.slice(0,100)}
                    ${inactive}
                    </h5>
                    <p class="card-text">${post.projectLeader }</p>
                    <p class="card-text small">${post.startDate }-${ post.endDate }</p>
                    <a href="/cms/project/${post._id}" class="btn btn-primary btn-sm"><i class="fas fa-edit mr-2"></i>Edit</a>
                    <a class="btn btn-danger text-light deleteBtn btn-sm" data-item-id=${post._id} data-resource="projects" data-toggle="modal" data-target="#deleteItemModal"><i class="fas fa-trash mr-2"></i>Delete</a>
                </div>
            </div>
        </div>`
    }
    

    document.getElementById('postListDiv').insertAdjacentHTML('beforeend', markup);
}

function loadPosts(posts, formType){
    for(let post of posts){
        //console.log('Loading post', post)
        postTemplate(post, formType);
        let btn = Array.from(document.getElementsByClassName('deleteBtn')).slice(-1)[0];
        //console.log(btn)
    }
}

function getPosts(){
    const fromDate = Array.from(document.getElementsByClassName('postDate')).slice(-1)[0].innerText;
    const formType=document.getElementById('postListDiv').dataset.formType
    axios.get(`/api/v1/${formType}?_createdAt={"$lt": "${fromDate}"}&$orderby={"_createdAt": -1}&limit=10`, {
        headers: {
        'content-type': 'application/json'
        }}).then(function (response) {
            if(response.data.status==='success'){
                loadPosts(response.data.data, formType)
            }
        })
        .catch(function (error) {
            //PRINT ERROR
            console.log(error);
        });
}

//detect when user scrolls to bottom
window.onscroll = function() {
    if ((window.innerHeight + Math.ceil(window.pageYOffset)) >= document.body.offsetHeight) {
        getPosts();
    }
}
