const log_enter = document.getElementById('log_enter');
const reg_enter = document.getElementById('reg_enter');
const logger = document.getElementById('logger');
const regger = document.getElementById('regger');
const reg_username = document.getElementById('reg_username');
const reg_pass = document.getElementById('reg_pass');
const reg_pass2 = document.getElementById('reg_pass2');
const reg_ok = document.getElementById('reg_ok');
const log_username = document.getElementById('log_username');
const log_pass = document.getElementById('log_pass');
const log_ok = document.getElementById('log_ok');

function show_login() {
    log_enter.classList.add('none');
    reg_enter.classList.remove('none');
    regger.classList.add('none');
    logger.classList.remove('none');
}

log_enter.onclick = function () {
    show_login()
}
reg_enter.onclick = function () {
    reg_enter.classList.add('none');
    log_enter.classList.remove('none');
    regger.classList.remove('none');
    logger.classList.add('none');
}
reg_ok.onclick = function () {
    if (!reg_username.value.trim() | !reg_pass.value.trim()) {
        alert('Нельзя пустые')
        return
    } else if (reg_pass.value != reg_pass2.value) {
        alert('Пароли не совпадают')
        return
    }

    const tosend = {
        username: reg_username.value,
        password: reg_pass.value
    };

    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(tosend)
    }).then(response => { return response.json(); })
        .then(data => {
            alert(data[0]);
            if (data[1] != 'success') {
                return
            } else {
                show_login()
            }
        });

}
log_ok.onclick = function () {
    if (!log_username.value.trim() | !log_pass.value.trim()) {
        alert('Нельзя пустые')
        return
    }

    const tosend = {
        username: log_username.value,
        password: log_pass.value
    };

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(tosend)
    }).then(response => { return response.json(); })
        .then(data => {

            if (data[1] != 'success') {
                alert(data[0]);
            } else {
                window.location.reload();
            }
        });

}