var loginBtn = document.getElementById('login');

loginBtn.addEventListener('click', (event) => {
    event.preventDefault();
    submitLoginData();
});

const form = document.getElementById("login-form");

async function submitLoginData() {
    const url = '/login/'
    const userData = {
        'username': null,
        'password': null,
    }

    userData.username = form.username.value;
    userData.password = form.password.value;

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'userData': userData
            }),
        });

        if (response.ok) {
            const responseData = await response.json();
            const accessToken = responseData['Access Token']
            sessionStorage.setItem("AccessToken", accessToken);            
            window.location.href = `/?Authorization=${accessToken}`;
        } else {
            window.alert("Your login information is not correct!");
        }
    } catch (error) {
        console.error('Error:', error);
    }
}