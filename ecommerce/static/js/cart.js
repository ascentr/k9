var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        var isMulti = false
        if (user == 'AnonymousUser') {
            addCookieItem(productId, action, isMulti)
        } else {
            updateUserOrder(productId, action, isMulti)
        }
    })
}



var multibuyBtns = document.getElementsByClassName('multi-to-cart')

for (i = 0 ; i< multibuyBtns.length; i++ ) {
    multibuyBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product
        var action = this.dataset.action
        var price = this.dataset.price
        var quantity = this.dataset.quantity
        var isMulti = true
        if (user == 'AnonymousUser') {
            addCookieItem(productId, action, price, quantity, isMulti)
        }
        else {
            updateUserOrder2(productId, action, price, quantity, isMulti) 
        }
    })

}


function addCookieItem(productId, action, price, quantity , isMulti){

    if (action == 'delete') {
        cart[productId] = {'quantity':0 }
        delete cart[productId]
    }

    if (action == 'add'){
        if (isMulti) {
            if (cart[productId]==undefined){
                cart[productId]={'quantity':parseInt(quantity)}
            } else {
                cart[productId]['quantity'] = parseInt(cart[productId]['quantity']) + parseInt(quantity) 
            }
        } else {
            if (cart[productId]==undefined){
                cart[productId]={'quantity':1}
            } else {
                cart[productId]['quantity'] += 1
            }
        }
    }

    if (action=='remove'){
        cart[productId]['quantity'] -= 1
        if ( cart[productId]['quantity'] <=0 ) {
            console.log('Item should be deleted')
            delete cart[productId]
        }
    }

    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    console.log('my cart ==>', cart)
    location.reload()
}

function updateUserOrder(productId, action, isMulti){
    console.log(user ,' is logged in ','productId:', productId, 'action:', action)

    var url = '/store/update_item/'
    fetch( url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json' ,
            'X-CSRFToken':csrftoken,

        } ,
        body:JSON.stringify({'isMulti':isMulti, 'productId':productId, 'action':action})
        
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data: ', data)
        location.reload()
    })
}

function updateUserOrder2(productId, action, price, quantity , isMulti ){
    var url = '/store/update_item/'
    fetch( url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json' ,
            'X-CSRFToken':csrftoken,

        } ,
        body:JSON.stringify({
            'isMulti':isMulti,
            'productId':productId, 
            'action':action , 
            'price':price, 
            'quantity':quantity
        })
        
    })
    .then((response) =>{
        return response.json()
    })
    .then((data) =>{
        console.log('data: ', data)
        location.reload()
    })
}
