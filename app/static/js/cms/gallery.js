import { showMessage }  from './statusMessage.js';
import {populateFieldErrors} from './fieldErrors.js';


let data = new FormData();
let count = Array.from(document.getElementsByClassName('galleryThumbnail')).length;

function loadFormData(data){

    data.append('title', document.getElementById('title').value);
    data.append('text', document.getElementById('text').value);

    let radioBtns=Array.from(document.getElementsByClassName('thumbnailRadioBtn'));
    for(let btn of radioBtns){
        if(btn.checked){
            data.append('coverImage', btn.dataset.thumbnail);
        }
    }

    return data
}


function submitGallery(requestType, galleryId='') {
    let url=`/api/v1/galleries`;
    if(requestType==='patch'){
        url=`/api/v1/galleries/${galleryId}`
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
                location.href = `/cms/galleries`
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
}


function imageThumbnail(file, count){
    let imgUrl = URL.createObjectURL(file);
    let markup=`
    <div class="col-xl-4 col-sm-12 p-2 galleryThumbnail newImage" id="preview_${count}" data-age="new">
        <div class="card card-common p-1">
            <div class="form-check text-center">
                <input class="form-check-input thumbnailRadioBtn" type="radio" data-age="new" id="thumbnail_${count}" name="galleryThumbnail" data-thumbnail="image_${count}" data-image-count="image_${count}">
                <label class="form-check-label" for="thumbnail_${count}">
                    set as thumbnail
                </label>
            </div>
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
        submitGallery('post')
    })
}


if(document.getElementById('submitEditForm')){
    document.getElementById('submitEditForm').addEventListener('click', function() {
        submitGallery('patch', this.dataset.postId)
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

}