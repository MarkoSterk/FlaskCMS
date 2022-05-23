
import { showMessage }  from './statusMessage.js';
import {populateFieldErrors} from './fieldErrors.js';

/////////////////////////////////////////////
//Change profile Image functionality//
const profileImageData = new FormData()
const userId=document.getElementById('currentUserName').dataset.userId;
let currentProfileImage=document.getElementById('userProfileImage').src

function changeProfileImage() {

    axios({
        method: 'patch',
        url: `/api/v1/users/update/${userId}`,
        data: profileImageData
      })
      .then(function (response) {
          if(response.data.status==='success'){
            showMessage(response.data.message, response.data.status);
            document.getElementById('profileImageUpload').value=null;
          }
          if(response.data.status==='error'){
            document.getElementById('userProfileImage').src=currentProfileImage;
            document.getElementById('profileImageUpload').value=null;
            showMessage(response.data.message, response.data.status)
          }
        
      })
      .catch(function (error) {
        //console.log(error.response.data)
        document.getElementById('userProfileImage').src=currentProfileImage;
        document.getElementById('profileImageUpload').value=null;
        showMessage(error.response.data.message, error.response.data.status)
      });
}

if(document.getElementById('profileImageUpload')){
    const imageInput = document.getElementById('profileImageUpload');
    imageInput.addEventListener('change', function(e) {
        const files = e.target.files // getting our files after upload
        profileImageData.delete('image');
        for (let file of files) {
            profileImageData.append('image', file) // appending file to form data
            document.getElementById('userProfileImage').src=URL.createObjectURL(file)
            document.getElementById('resetChangeProfileImage').style.display='inline';
        }
    });
}

if(document.getElementById('submitChangeProfileImage')){
    const submitProfileImageBtn=document.getElementById('submitChangeProfileImage');
    submitProfileImageBtn.addEventListener('click', function() {
        changeProfileImage();
    })
}

if(document.getElementById('resetChangeProfileImage')){
    const resetProfileImageBtn=document.getElementById('resetChangeProfileImage');
    resetProfileImageBtn.addEventListener('click', function() {
        document.getElementById('userProfileImage').src=currentProfileImage;
        document.getElementById('changeProfileImageForm').reset();
        this.style.display='none';
    })
}
//End of change profile image functionality//
/////////////////////////////////////////////

function changePassword() {
    const passwordData = new FormData()

    passwordData.append('currentPassword', document.getElementById('currentPassword').value)
    passwordData.append('newPassword', document.getElementById('password').value)
    passwordData.append('confirmNewPassword', document.getElementById('confirmNewPassword').value)

    axios({
        method: 'patch',
        url: `/api/v1/users/updatePassword/${userId}`,
        data: passwordData
      })
      .then(function (response) {
          if(response.data.status==='success'){
            showMessage(response.data.message, response.data.status)
            document.getElementById('changePasswordForm').reset()
          }
          if(response.data.status==='error'){
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

if(document.getElementById('submitChangePassword')){
    document.getElementById('submitChangePassword').addEventListener('click', function() {
        changePassword();
    })
}







