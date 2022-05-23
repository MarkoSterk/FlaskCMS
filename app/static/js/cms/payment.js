function downloadPayment(){
    const paymentId=document.getElementById('modalPaymentId').innerText;
    axios.get(`/api/v1/payments/download/${paymentId}`, {
        responseType: 'arraybuffer'
      }).then(function (response) {
            const blob = new Blob(
                [response.data],
                { type: 'application/pdf' }
            )
            const url = window.URL.createObjectURL(blob);
            window.open(url) ;
        })
        .catch(function (error) {
            //PRINT ERROR
            console.log(error);
        });
}



function loadPaymentDetails(paymentId){
    axios.get(`/api/v1/payments/${paymentId}`, {
        headers: {
        'content-type': 'application/json'
        }}).then(function (response) {
            if(response.data.status==='success'){
                const paymentData = response.data.data[0];
                document.getElementById('modalPaymentId').innerHTML=paymentData.purchaseId;
                document.getElementById('modalClientEmail').innerHTML=paymentData.client;
                document.getElementById('modalDateOfPurchase').innerHTML=paymentData._createdAt;
                document.getElementById('modalProductName').innerHTML=paymentData.productId.name;
                document.getElementById('modalProductDescription').innerHTML=paymentData.productId.text;
                document.getElementById('modalAmountTotal').innerHTML=paymentData.amountTotal;
                document.getElementById('modalCurrency').innerHTML=paymentData.currency;
            }
        })
        .catch(function (error) {
            //PRINT ERROR
            console.log(error);
        });
}


$('#payment-details').on('shown.bs.modal', function (e) {
    const btn = e.relatedTarget;
    loadPaymentDetails(btn.dataset.purchaseId);
});

document.getElementById('downloadPaymentBtn').addEventListener('click', function() {
    downloadPayment();
})