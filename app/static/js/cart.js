function addToCart(id, name, price){
    event.preventDefault()

    fetch('/api/add-cart', {
        method: 'post',
        body: JSON.stringify({
            'id': id,
            'name': name,
            'price': price
        }),
        headers:{
            'Content-Type': 'application/json'
        }
    }).then(function (response) {
        console.info(response)
        return response.json()
    }).then(function (data){
        console.info(data)

        let counter = document.getElementById('cartCounter')
        counter.innerText= data.total_quantity
    }).catch(function(error){
        console.error(error)
    })
}

function pay()
{
    if (confirm('Ban chac chan muon thanh toan?') == true){
        fetch('/api/pay', {
        method: 'post',
        }).then(res =>res.json()).then(data =>{
            if(data.code == 200)
                location.reload()
        }).catch(error =>console.error(error))
    }
}