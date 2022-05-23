function createCheckoutSession(stripe, product) {
  const data = {
    price: product.dataset.price,
    quantity: product.dataset.quantity,
    name: product.dataset.name,
    productId: product.dataset.productId,
    image: product.dataset.image
  }
  axios({
      method: 'post',
      url: '/api/v1/payments/create-checkout-session',
      data: data
    })
    .then(function (response) {
      //console.log(response.data)
      return stripe.redirectToCheckout({sessionId: response.data.sessionId})
    })
    .catch(function (error) {
      console.log('Error')
    });
}


const purchaseBtns = Array.from(document.getElementsByClassName('purchase'));

purchaseBtns.forEach((btn) => {
  btn.addEventListener('click', function() {
    initializeStripe(this)
  });
});

function initializeStripe(product){
    axios({
        method: 'get',
        url: '/api/v1/payments/config'
      })
      .then(function (response) {
        const stripe = Stripe(response.data.publicKey);
        createCheckoutSession(stripe, product);

      })
      .catch(function (error) {
        console.log('Error')
      });
};