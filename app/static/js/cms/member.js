import { showMessage }  from './statusMessage.js';
import {populateFieldErrors} from './fieldErrors.js';

let data = new FormData();

function loadFormData(data){
    const elements = document.getElementsByClassName('form-control');
    for(let element of elements){
        if(element.id==='image'){
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
    return data
}

function submitForm(requestType, memberId='') {

    let url=`/api/v1/members`;
    if(requestType==='patch'){
        url=`/api/v1/members/${memberId}`
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
            document.getElementById('memberForm').reset()
            showMessage(response.data.message, response.data.status)
            window.setTimeout(function() {
                location.href = '/cms/members'
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

function removeMemberImage(){
    document.getElementById('previewImage').src='';
    document.getElementById('image').style.display='block';
    document.getElementById('previewBlock').style.display='none';
    data.delete('image');
    data.append('image', '_DELETE');
    document.getElementById('image').value='';
    // for(var pair of data.entries()) {
    //     console.log(pair[0]+ ', '+ pair[1]);
    //  }

}

// function deleteMember(memberId){
//     window.scrollTo(0,0);
//     axios.delete(
//         `/api/v1/members/${memberId}`
//     )
//     .then(function (response) {
//         if(response.status == 204){
//             showMessage('Team member deleted successfully', 'success')
//             var elem = document.getElementById(`memberCard_${memberId}`);
//             elem.parentNode.removeChild(elem);
//         }
//     })
//     .catch(function (error) {
//         console.log(error)
//     });
// }

if(document.getElementById('resetMemberForm')){
    const resetBtn = document.getElementById('resetMemberForm');
    resetBtn.addEventListener('click', function() {
        document.getElementById('memberForm').reset();
    })
}

if(document.getElementById('submitMemberForm')){
    const submitBtn = document.getElementById('submitMemberForm');
    submitBtn.addEventListener('click', function() {
        submitForm('post');
    });
}

if(document.getElementById('submitEditMemberForm')){
    const submitBtn = document.getElementById('submitEditMemberForm');
    submitBtn.addEventListener('click', function() {
        submitForm('patch', this.dataset.memberId);
    });
}

if(document.getElementById('removeImage')){
    const removeImgBtn = document.getElementById('removeImage');
    removeImgBtn.addEventListener('click', function() {
        removeMemberImage();
    });
}

if(document.getElementById('image')){
    const imageInput = document.getElementById('image');
    imageInput.addEventListener('change', function(e) {
    const files = e.target.files // getting our files after upload
    data.delete('image');
    for (const file of files) {
        data.append('image', file) // appending every file to formdata
        document.getElementById('previewImage').src = URL.createObjectURL(file);
        document.getElementById('previewBlock').style.display = 'block';
        document.getElementById('image').style.display = 'none';
        }
    });
}


// if(location.href.endsWith('/members')){
//     const delBtns = document.getElementsByClassName('deleteMemberBtn');
//     for(let btn of delBtns){
//         btn.addEventListener('click', function() {
//             deleteMember(this.dataset.memberId);
//         });
//     }
// }

