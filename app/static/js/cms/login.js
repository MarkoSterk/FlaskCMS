import { showMessage }  from './statusMessage.js';


function login() {

    const data = new FormData()
    data.append('email', document.getElementById('email-input').value);
    data.append('password', document.getElementById('password-input').value);

    axios({
        method: 'post',
        url: '/api/v1/users/login',
        data
      })
      .then(function (response) {
        if(response.data.status==='success'){
            document.getElementById('login-form').reset()
            window.setTimeout(function() {
                location.href = '/cms'
            }, 3000);
        }
        showMessage(response.data.message, response.data.status)
      })
      .catch(function (error) {
        //console.log(error.response.data)
        showMessage(error.response.data.message, error.response.data.status)
      });
}



const loginBtn = document.getElementById('login-btn');
loginBtn.addEventListener('click', function(){
    login();
})



