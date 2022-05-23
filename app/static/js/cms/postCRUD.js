import { showMessage }  from './statusMessage.js';
import {populateFieldErrors} from './fieldErrors.js';

let data = new FormData();

function loadFormData(data){
    const elements = document.getElementsByClassName('form-control');
    for(let element of elements){
        if(element.id==='coverImage'){
            if(element.files.length>0){
                data.append(element.id, element.files[0]);
            }
        }
        else{
            if(element.value.length>0){
                data.append(element.id, element.value)
            }
        }
    };

    const categories = document.getElementsByClassName('form-check-input')
    if(categories.length>0){
        let catList=[]
        for(let cat of categories){
            if(cat.checked){
                catList.push(cat.value)
            }
        }
        if(catList.length>0){
            data.append('category', catList.join(','))
        }
    }

    return data
}

function submitForm(requestType, formType, postId='') {

    let url=`/api/v1/${formType}`;
    if(requestType==='patch'){
        url=`/api/v1/${formType}/${postId}`
    }

    data = loadFormData(data)
    window.scrollTo(0,0);
    axios({
        method: requestType,
        url: url,
        data
      })
      .then(function (response) {
        if(response.data.status==='success'){
            document.getElementById('postForm').reset()
            showMessage(response.data.message, response.data.status)
            window.setTimeout(function() {
                location.href = `/cms/${formType}`
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


// export function deletePost(postId, formType){
//     window.scrollTo(0,0);
//     axios.delete(
//         `/api/v1/${formType}/${postId}`
//     )
//     .then(function (response) {
//         if(response.status == 204){
//             showMessage('Deleted successfully', 'success')
//             var elem = document.getElementById(`card_${postId}`);
//             elem.parentNode.removeChild(elem);
//         }
//     })
//     .catch(function (error) {
//         showMessage(error.response.data.message, error.response.data.status)
//     });
// }

function removeCoverImage(){
    document.getElementById('previewImage').src='';
    document.getElementById('coverImage').style.display='block';
    document.getElementById('previewBlock').style.display='none';
    data.delete('coverImage');
    data.append('coverImage', '_DELETE');
    document.getElementById('coverImage').value='';
    // for(var pair of data.entries()) {
    //     console.log(pair[0]+ ', '+ pair[1]);
    //  }

}


if(document.getElementById('submitForm')){
    const submitBtn = document.getElementById('submitForm');
    submitBtn.addEventListener('click', function() {
        submitForm('post', this.dataset.formType);
    });
}


if(document.getElementById('submitEditForm')){
    const submitBtn = document.getElementById('submitEditForm');
    submitBtn.addEventListener('click', function() {
        submitForm('patch', this.dataset.formType, this.dataset.postId);
    });
}

if(document.getElementById('resetForm')){
    const resetBtn = document.getElementById('resetForm');
    resetBtn.addEventListener('click', function() {
        document.getElementById('postForm').reset();
    })
}


if(document.getElementById('removeImage')){
    const removeImgBtn = document.getElementById('removeImage');
    removeImgBtn.addEventListener('click', function() {
        removeCoverImage();
    });
}


if(document.getElementById('coverImage')){
    const imageInput = document.getElementById('coverImage');
    imageInput.addEventListener('change', function(e) {
        const files = e.target.files // getting our files after upload
        data.delete('coverImage');
        for (const file of files) {
            data.append('coverImage', file) // appending every file to formdata
            document.getElementById('previewImage').src = URL.createObjectURL(file);
            document.getElementById('previewBlock').style.display = 'block';
            document.getElementById('coverImage').style.display = 'none';
        }
    });
}

// if(location.href.endsWith('/projects') || location.href.endsWith('/posts') || location.href.endsWith('/publications') || location.href.endsWith('galleries')){
//     const delBtns = document.getElementsByClassName('deleteBtn');
//     for(let btn of delBtns){
//         btn.addEventListener('click', function() {
//             deletePost(this.dataset.postId, this.dataset.formType);
//         });
//     }
// }