import { showMessage }  from './statusMessage.js';
import {populateFieldErrors} from './fieldErrors.js';


let data = new FormData();
let count = Array.from(document.getElementsByClassName('galleryThumbnail')).length;

function loadFormData(data){

    data.append('name', document.getElementById('name').value);
    data.append('text', document.getElementById('text').value);
    data.append('price', document.getElementById('price').value);
    data.append('quantity', document.getElementById('quantity').value);

    return data
}


function submitProduct(requestType, productId='') {
    let url=`/api/v1/products`;
    if(requestType==='patch'){
        url=`/api/v1/products/${productId}`
    }

    data = loadFormData(data);

    window.scrollTo(0,0);
    axios({
        method: requestType,
        url: url,
        data
      })
      .then(function (response) {
        if(response.data.status==='success'){
            showMessage(response.data.message, response.data.status)
            window.setTimeout(function() {
                location.href = `/cms/products`
            }, 3000);
        }
        else if(response.data.status==='error'){
            showMessage(response.data.message, response.data.status)
        }
        else{
            populateFieldErrors(response.data.message)
        }
      })
      .catch(function (error) {
        showMessage(error.response.data.message, error.response.data.status)
      });
};


function imageThumbnail(file, count){
    let imgUrl = URL.createObjectURL(file);
    let markup=`
    <div class="col-xl-4 col-sm-12 p-2 galleryThumbnail newImage" id="preview_${count}" data-age="new">
        <div class="card card-common p-1">
            <img src=${imgUrl} class="card-img-top img-thumbnail galleryImage m-auto" data-age="new" style="max-height: 300px; max-width: 300px;" alt="gallery image">

            <div class="card-body">
                <button type="button" class="btn btn-danger btn-sm deleteThumbnail" data-target="image_${count}" data-count=${count}>Remove</button>
            </div>
        </div>
    </div>`
    return markup;
}


function removeThumbnail(btn){
    data.delete(btn.dataset.target);
    let elem = document.getElementById(`preview_${btn.dataset.count}`)
    elem.parentElement.removeChild(elem);
}


function loadThumbnails(file, count) {
    document.getElementById('imageThumbnails').insertAdjacentHTML('beforeend', imageThumbnail(file, count));
}


if(document.getElementById('images')){
    document.getElementById('images').addEventListener('change', function(e) {

        const newImages=Array.from(document.getElementsByClassName('newImage'));
        for(let image of newImages){
            Array.from(image.getElementsByClassName('deleteThumbnail'))[0].click();
        }

        const files = e.target.files // getting files after upload
        for (let file of files) {
            loadThumbnails(file, count);
            data.append(`image_${count}`, file);
            count++;
        }
        const delBtns = Array.from(document.getElementsByClassName('deleteThumbnail'))
        for(let btn of delBtns){
            btn.addEventListener('click', function() {
                removeThumbnail(this);
            })
        }
    })
}


for(let btn of Array.from(document.getElementsByClassName('deleteThumbnail'))){
    btn.addEventListener('click', function() {
        removeThumbnail(this);
    })
}

if(document.getElementById('submitForm')){
    document.getElementById('submitForm').addEventListener('click', function() {
        submitProduct('post')
    })
}


if(document.getElementById('submitEditForm')){
    document.getElementById('submitEditForm').addEventListener('click', function() {
        submitProduct('patch', this.dataset.postId)
    })
}


if(document.getElementsByClassName('oldImage')){
    const oldImages = Array.from(document.getElementsByClassName('oldImage'));
    //console.log(oldImages)
    let oldCount = 0;
    for(let image of oldImages){
        //console.log(image)
        let imageName = Array.from(image.getElementsByClassName('galleryImage'))[0].src.split('/').slice(-1)[0];
        //console.log(imageName)
        data.append(`oldImage_${oldCount}`, imageName);
        oldCount++;
    }

};



// function deleteProduct(productId){
//     window.scrollTo(0,0);
//     axios.delete(
//         `/api/v1/products/${productId}`
//     )
//     .then(function (response) {
//         if(response.status == 204){
//             showMessage('Deleted successfully', 'success')
//             var elem = document.getElementById(`card_${productId}`);
//             elem.parentNode.removeChild(elem);
//         }
//     })
//     .catch(function (error) {
//         showMessage(error.response.data.message, error.response.data.status)
//     });
// }


// const delBtns = Array.from(document.getElementsByClassName('deleteBtn'));
// delBtns.forEach((btn) => {
//     btn.addEventListener('click', function(){
//         deleteProduct(this.dataset.postId)
//     });
// });










if(document.getElementsByClassName('oldImage')){
    const oldImages = Array.from(document.getElementsByClassName('oldImage'));
    //console.log(oldImages)
    let oldCount = 0;
    for(let image of oldImages){
        //console.log(image)
        let imageName = Array.from(image.getElementsByClassName('galleryImage'))[0].src.split('/').slice(-1)[0];
        //console.log(imageName)
        data.append(`oldImage_${oldCount}`, imageName);
        oldCount++;
    }

}