var signupBtns = document.getElementById('signup');
signupBtns.addEventListener('click', (event) => {
    event.preventDefault();
    submitSignupData();
});

const form = document.getElementById("signup-form");

async function submitSignupData() {
    const url = '/create_user/'
    const userData = {
        'username': null,
        'email': null,
        'password': null,
        'password_confirm': null,
    }

    userData.username = form.username.value;
    userData.email = form.email.value;
    userData.password = form.password.value;
    userData.password_confirm = form.password_confirm.value;

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

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const responseData = await response.json();
        console.log("Created user successfully :", responseData);
        window.location.href = "/view_login/"
    } catch (error) {
        console.error('Error:', error);
    }
}