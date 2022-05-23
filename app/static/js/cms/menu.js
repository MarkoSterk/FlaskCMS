import { showMessage }  from './statusMessage.js';
import {populateFieldErrors} from './fieldErrors.js';

function menuItemTemplate(id, link, linkTarget, name, checked){
    return `
    <div id="${id}" draggable="true" class="container-fluid draggable dropzone m-0 px-0 py-1 w-100" dropzone="true">
        <div class="d-flex justify-content-between align-items-center border border-dark rounded text-light bg-primary m-auto mt-1 p-1">
            <p class="h5 m-0 d-inline elemName" data-link="${link}" data-link-target="${linkTarget}">${name}</p>
            <div class="d-inline m-0 p-0">
                <p class="m-0 mr-1 py-0 px-1 d-inline border border-dark rounded btn btn-secondary text-center text-light downArrow"><i class="fas fa-arrow-alt-circle-down m-0 p-0"></i></>
                <p class="m-0 mr-1 py-0 px-1 d-inline border border-dark rounded btn btn-secondary text-center text-light upArrow"><i class="fas fa-arrow-alt-circle-up m-0 p-0"></i></>
                <p class="m-0 mr-1 py-0 px-1 d-inline border border-dark rounded btn btn-secondary text-center text-light editBtn"><i class="fas fa-edit m-0 p-0"></i></>
                <p class="m-0 mr-1 py-0 px-1 d-inline border border-dark rounded btn btn-secondary text-center text-light deleteBtn"><i class="fas fa-trash m-0 p-0"></i></p>
            </div>
        </div>
        <div class="editElement mx-1 bg-light p-1 border border-dark border-top-0" style="display: none;">
            <form>
                <div class="form-group">
                    <label>Link name:</label>
                    <input type="text" class="form-control editNameInput" value=${name}>
                </div>
                <div class="form-group">
                    <label>Link address:</label>
                    <input type="text" class="form-control editLinkInput" value=${link}>
                </div>
                <div class="form-check form-group">
                  ${checked}
                  <label class="form-check-label" for="linkTarget_${id}">
                    Open link in new window
                  </label>
                </div>
                <div class="form-group">
                    <button type="button" class="btn btn-primary btn-sm submitEditBtn">Ok</button>
                    <button type="button" class="btn btn-secondary btn-sm cancelEditBtn">Cancel</button>
                </div>
            </form>
        </div>
        <div class="subItems ml-5" id="subItems_${id}">

        </div>
    </div>
    `
}


function configureMenuItem(div, id){
    let delBtn=Array.from(div.getElementsByClassName('deleteBtn'))[0];
    let editBtn=Array.from(div.getElementsByClassName('editBtn'))[0];
    let submitEditBtn=Array.from(div.getElementsByClassName('submitEditBtn'))[0];
    let cancelEditBtn=Array.from(div.getElementsByClassName('cancelEditBtn'))[0];
    let arrowUp=Array.from(div.getElementsByClassName('upArrow'))[0];
    let arrowDown=Array.from(div.getElementsByClassName('downArrow'))[0];

    submitEditBtn.addEventListener('click', function(){
        editMenuItem(div);
        toggleVisibility(div);
    })

    cancelEditBtn.addEventListener('click', function() {
        cancelEditMenuItem(div);
        toggleVisibility(div);
    })

    arrowUp.addEventListener('click', function() {
        moveUp(id);
    })

    arrowDown.addEventListener('click', function() {
        moveDown(id);
    })

    delBtn.addEventListener('click', function(){
        deleteElement(div);
    })

    editBtn.addEventListener('click', function() {
        toggleVisibility(div);
    })


    div.addEventListener('dragstart', function(e){
        e.stopPropagation();
        onDragStart(this, e);
    }, false)

    div.addEventListener('dragend', function(e){
        e.stopPropagation();
        onDragEnd(this, e);
    }, false)

    div.addEventListener('drag', function(e) {
        e.stopPropagation();
        // console.log(e.target.id)
    }, false)

    div.addEventListener('dragenter', function(e) {
        e.stopPropagation();
        if(this != e.target){
            e.target.style.opacity=0.5;
        }
    }, false)

    div.addEventListener('dragleave', function(e) {
        e.stopPropagation();
        e.target.style.opacity=1.0;
    }, false)

    div.addEventListener('dragover', function(e) {
        e.preventDefault();
        e.stopPropagation();
    }, false)

    div.addEventListener('drop', function(e) {
        e.preventDefault();
        e.stopPropagation();
        e.target.style.opacity=1.0;
        const dragging = document.querySelector('.dragging');
        // console.log(e.target);
        // console.log(dragging);
        const targetZone = e.target.parentElement.querySelector('.subItems')
        if(dragging!=targetZone.parentElement){
            targetZone.appendChild(dragging);
        }   
    }, false)
}


function toggleVisibility(container){
    const editDiv=Array.from(container.getElementsByClassName('editElement'))[0]
    const allDivs = Array.from(document.getElementsByClassName('editElement'));
    allDivs.forEach(div => {
        if(div!=editDiv){
            div.style.display='none';
        } 
    })
    
    if(editDiv.style.display==='none'){
        editDiv.style.display='block'
    }
    else {
        editDiv.style.display='none';
    }
}

function deleteElement(container){
    container.parentNode.removeChild(container);
}

function editMenuItem(container){
    const item = Array.from(container.getElementsByClassName('elemName'))[0];
    const newName = Array.from(container.getElementsByClassName('editNameInput'))[0].value;
    const newLink = Array.from(container.getElementsByClassName('editLinkInput'))[0].value;

    item.innerHTML = newName;
    item.dataset.link = newLink;
}

function cancelEditMenuItem(container){
    const item = Array.from(container.getElementsByClassName('elemName'))[0];
    const inputName = Array.from(container.getElementsByClassName('editNameInput'))[0];
    const inputLink = Array.from(container.getElementsByClassName('editLinkInput'))[0];

    inputName.value = item.innerHTML;
    inputLink.value = item.dataset.link;
}

function onDragStart(draggable, e){
    draggable.classList.add('dragging');
}

function onDragEnd(draggable, e){
    draggable.classList.remove('dragging');
}


function moveUp(id){
    //console.log('up');
    var node=document.getElementById(id)
    var parent = node.parentElement;

    if(node.previousElementSibling){
        parent.insertBefore(node, node.previousElementSibling);
    }
}

function moveDown(id){
    //console.log('down');
    var node=document.getElementById(id)
    var parent = node.parentElement;

    if(node.nextElementSibling){
        parent.insertBefore(node.nextElementSibling, node);
    }
    
}


function createMenuElement(){
    let id=Date.now()
    let name=document.getElementById('elemName').value;
    let link=document.getElementById('elemLink').value;
    let linkTarget='_self';
    let checked=`<input class="form-check-input" type="checkbox" value="_blank" id="linkTarget_${id}"></input>`
    if(document.getElementById('linkTarget').checked){
        linkTarget='_blank';
        checked=`<input class="form-check-input" type="checkbox" value="_blank" id="linkTarget_${id}" checked></input>`
    }
    
    let markup=menuItemTemplate(id, link, linkTarget, name, checked)

    menuTree.insertAdjacentHTML('beforeend', markup);
    
    let lastDiv = Array.from(menuTree.getElementsByClassName('draggable')).slice(-1)[0];
    configureMenuItem(lastDiv, id);
}


const menuTree=document.getElementById('menuTree');
const addElem=document.getElementById('addElementBtn');
const saveMenuBtn=document.getElementById('saveMenuStructure');
const deleteMenuBtn=document.getElementById('deleteMenuStructure');

menuTree.addEventListener('drop', function(e){
    e.preventDefault();
    e.stopPropagation();
    
    const dragging = document.querySelector('.dragging');
    this.appendChild(dragging);
});

menuTree.addEventListener('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation()
});

addElem.addEventListener('click', function(){
    createMenuElement();
    document.getElementById('addMenuElement').reset();
})

saveMenuBtn.addEventListener('click', function() {
    parseMenuStructure('menuTree');
})

deleteMenuBtn.addEventListener('click', function(){
    deleteMenu();
})

function saveMenu(data){
    window.scrollTo(0,0);
    axios({
        method: 'post',
        url: '/api/v1/menu/save',
        data
      })
      .then(function (response) {
        showMessage(response.data.message, response.data.status);
        window.setTimeout(function() {
            location.reload();
        }, 1000);
      })
      .catch(function (error) {
        //console.log(error.response.data)
        showMessage(error.response.data.message, error.response.data.status)
      });

}

function parseMenuStructure(id){
    const menuTree = document.getElementById(id);
    const allElements = Array.from(menuTree.getElementsByClassName('draggable'));

    const menuStructure = [];
    let count = 0;

    for(let element of allElements){
        menuStructure.push({});
        if(element.parentNode.id==id){
            menuStructure[count]['parentId']='topLevel';
        }
        else{
            menuStructure[count]['parentId']=element.parentNode.parentNode.id
        }
        //<p class="h5 m-0 d-inline elemName" data-link="${link}" data-link-target="${linkTarget}">${name}</p>
        menuStructure[count]['itemId']=element.id;
        let elemName = Array.from(element.getElementsByClassName('elemName'))[0].innerText;
        let elemLink = Array.from(element.getElementsByClassName('elemName'))[0].dataset.link;
        let elemLinkTarget = Array.from(element.getElementsByClassName('elemName'))[0].dataset.linkTarget;
        
        menuStructure[count]['name']=elemName;
        menuStructure[count]['link']=elemLink;
        menuStructure[count]['linkTarget']=elemLinkTarget;
        count++;
    }
    saveMenu(menuStructure);
}

function deleteMenu(){
    window.scrollTo(0,0);
    axios.delete(
        `/api/v1/menu/delete`
    )
    .then(function (response) {
        if(response.status == 204){
            showMessage('Menu deleted successfully', 'success')
            window.setTimeout(function() {
                location.reload();
            }, 1000);
        }
        else{
            showMessage('Something went wrong', 'error')
        }
    })
    .catch(function (error) {
        showMessage(error.response.data.message, error.response.data.status)
    });
}

function getMenu(){
    axios.get(`/api/v1/menu/load`, {
        headers: {
        'content-type': 'application/json'
        }}).then(function (response) {
            if(response.data.status==='success'){
                loadMenu(response.data.data)
            }
            else{
                showMessage(response.data.message, response.data.status)
            }
        })
        .catch(function (error) {
            showMessage(error.response.data.message, error.response.data.status)
        });
}

function loadMenu(menu){
    if(menu.name==='default'){
        deleteMenuBtn.style.display='none';
    };
    
    const menuTree = document.getElementById('menuTree');
    for(let elem of menu.structure){
        let checked=`<input class="form-check-input" type="checkbox" value="_blank" id="linkTarget_${elem.itemId}"></input>`
        if(elem.linkTarget==='_blank'){
            checked=`<input class="form-check-input" type="checkbox" value="_blank" id="linkTarget_${elem.itemId}" checked></input>`
        }

        let markup=menuItemTemplate(elem.itemId, elem.link, elem.linkTarget, elem.name, checked)
        let lastDiv;

        if(elem.parentId === 'topLevel'){
            menuTree.insertAdjacentHTML('beforeend', markup);
            lastDiv = Array.from(menuTree.getElementsByClassName('draggable')).slice(-1)[0];
        }
        else{
            let parent = document.getElementById(`subItems_${elem.parentId}`)
            parent.insertAdjacentHTML('beforeend', markup);
            lastDiv = Array.from(parent.getElementsByClassName('draggable')).slice(-1)[0];
        }

        configureMenuItem(lastDiv, elem.itemId);
        
    }
}

getMenu();
