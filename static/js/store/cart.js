var updateBtns = document.getElementsByClassName('update-cart');
var loginBtn = document.getElementById('login');
var logoutBtn = document.getElementById('logout');
var signupBtn = document.getElementById('signup');

for (var i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var productId = this.dataset.product;
        var action = this.dataset.action;

        console.log("productId: ", productId, "Action: ", action);
        console.log("USER: ", user);
        
        if (user === "AnonymousUser") {
            console.log('User is not authenticated');
        } else {
            updateUserOrder(productId, action);            
        }
    });
}

const updateUserOrder = (productId, action) => {
    console.log("User is logged in, sending data...");

    var url = '/update_item/';   

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': sessionStorage.getItem("AccessToken") || "",
            // 'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action,
        }),
    }).then((response) => {
        return response.json();
    }).then((data) => {
        console.log('data: ', data);
        location.reload();
    });
}

async function logout() {
    const url = '/logout/'

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
        });

        if (response.ok) {
            window.location.href = `/`;
        } else {
            window.alert("Something went wrong!");
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

if (sessionStorage.getItem('AccessToken') != null) {
    console.log(sessionStorage.getItem('AccessToken'));
    loginBtn.style.display = 'none';
    signupBtn.style.display = 'none';
    logoutBtn.style.display = 'block'; 
}

logoutBtn.addEventListener('click', (event) => {
    logout();
    sessionStorage.clear();
});

