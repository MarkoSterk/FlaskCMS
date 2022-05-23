import { showMessage }  from './statusMessage.js';

$('#deleteItemModal').on('shown.bs.modal', function (e) {
    const btn = e.relatedTarget;
    document.getElementById('delete-item').dataset.itemId=btn.dataset.itemId
    document.getElementById('delete-item').dataset.resource=btn.dataset.resource
});

document.getElementById('delete-item').addEventListener('click', function() {
    deleteItem(this.dataset.itemId, this.dataset.resource)
})


export function deleteItem(itemId, resource){
    window.scrollTo(0,0);
    axios.delete(
        `/api/v1/${resource}/${itemId}`
    )
    .then(function (response) {
        if(response.status == 204){
            showMessage('Deleted successfully', 'success')
            var elem = document.getElementById(`card_${itemId}`);
            elem.parentNode.removeChild(elem);
        }
    })
    .catch(function (error) {
        showMessage(error.response.data.message, error.response.data.status)
    });
}

