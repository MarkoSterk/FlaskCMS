function createTag(text){
    let markup=`<button class="btn btn-secondary mx-1" type="button"><span class="tagText mr-1">${text.toUpperCase().trim()}</span><span class="closeTag ml-1">&#10006;</span></button>`;

    document.getElementById('tagsList').insertAdjacentHTML('beforeend', markup);
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

document.getElementById('tagsInput').addEventListener("keyup", function(event) {
    if(event.code === 'Enter' || event.code === 'Space'){
        createTag(this.value);
        this.value='';

        let tag = Array.from(document.getElementsByClassName('closeTag')).slice(-1)[0];
        tag.addEventListener('click', function() {
            removeTag(this);
        })
    }
});