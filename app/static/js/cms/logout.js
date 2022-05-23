import { showMessage }  from './statusMessage.js';


function logout() {

    axios({
        method: 'get',
        url: '/api/v1/users/logout'
      })
      .then(function (response) {
        if(response.data.status==='success'){
            window.setTimeout(function() {
                location.href = '/cms/login'
            }, 1000);
        }
        showMessage(response.data.message, response.data.status)
      })
      .catch(function (error) {
        //console.log(error.response.data)
        showMessage(error.response.data.message, error.response.data.status)
      });
}



const loginBtn = document.getElementById('logout-btn');
loginBtn.addEventListener('click', function(){
    logout();
})



