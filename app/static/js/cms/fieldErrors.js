export const removeFieldErrors = () => {
    const fields = document.querySelectorAll('.field-error');

    fields.forEach(field => {
        field.remove();
    });
}


export const populateFieldErrors = (fields) => {

    removeFieldErrors();

    for(let field of fields){
        const [key] = Object.entries(field);
        let markup = `<p class="text-danger text-left small field-error">${key[1][0]}: ${key[1][1]}</p>`
        document.getElementById(key[0]).parentElement.insertAdjacentHTML('beforeend', markup);
    }

    // const markup = `<div class="alert text-center p-3 mb-2 mt-5 ${msgClass}">${msg}</div>`
    // document.querySelector('body').insertAdjacentHTML('afterbegin', markup);

    // window.setTimeout(hideMessage, time * 1000);
};
