function createTag(text){
    if(text.length>0 && text!=' '){
        let markup=`<button class="btn btn-secondary mx-1" type="button"><span class="tagText mr-1">${text.toUpperCase().trim()}</span><span class="closeTag ml-1">&#10006;</span></button>`;

        document.getElementById('tagsList').insertAdjacentHTML('beforeend', markup);

        let tag = Array.from(document.getElementsByClassName('closeTag')).slice(-1)[0];
        tag.addEventListener('click', function() {
            removeTag(this);
        });
    }
}

function removeTag(tag){
    tag.parentNode.parentNode.removeChild(tag.parentNode);
}

export function readTags(){
    let tagsValues = [];
    let tags = Array.from(document.getElementsByClassName('tagText'));
    for(let tag of tags){
        tagsValues.push(tag.innerText);
    }
    return tagsValues;
}

export function loadTags(){
    let tags = Array.from(document.getElementsByClassName('closeTag'));
    for(let tag of tags){
        tag.addEventListener('click', function() {
            removeTag(this);
        })
    }
}

if(document.getElementById('tagsInput')){
    document.getElementById('tagsInput').addEventListener("keyup", function(event) {
        if(event.code === 'Enter' || event.code === 'Space'){
            event.preventDefault();
            createTag(this.value);
            this.value='';
        }
    });
}
