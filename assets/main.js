document.querySelectorAll('#tasks .card').forEach(card => {
    const btn = card.querySelector('.btn-red');
    const br = card.querySelector('br');
    btn.addEventListener('click', () => {
        console.log('CLICK!!!')
        card.classList.add('hidden')
        doneContainer.prepend(card);
        card.removeChild(btn)
        card.removeChild(br)
        requestAnimationFrame(() => {
            card.classList.remove('hidden')
        });
        fetch('/del_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: card.id })
        })
    })
}) // к кнопкам которые при заходе на страницу

var cards = 0;
adder = document.querySelector('#add_task')
const cardsContainer = document.getElementById("tasks");
const doneContainer = document.getElementById("done_tasks");
const name_inp = document.getElementById('name')
const descrip = document.getElementById('description');
const datetime = document.getElementById('datetime');

// создание в живую
adder.onclick = function () {
    cards += 1
    if (!descrip.value || !name_inp.value) { alert("Забыли кое-что"); return }
    if (!datetime.value) { datetime.value = 'нету' }

    const br = document.createElement('br');
    const br2 = document.createElement('br');

    const newCard = document.createElement("div");
    newCard.className = "card hidden";

    const title = document.createElement('h4');
    title.className = "title";
    title.textContent = name_inp.value;

    const body = document.createElement('div');
    body.className = 'descrip';
    body.textContent = descrip.value;


    const deadline = document.createElement('label');
    deadline.className = 'when';
    deadline.textContent = `Дедлайн: ${datetime.value}`;

    const btn = document.createElement('div');
    btn.className = 'btn btn-red';
    btn.textContent = 'Закрыть задачу';

    btn.addEventListener('click', () => {
        newCard.classList.add('hidden')
        doneContainer.prepend(newCard);

        newCard.removeChild(btn)
        newCard.removeChild(br2)

        requestAnimationFrame(() => {
            newCard.classList.remove('hidden')
        });
        fetch('/del_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: newCard.id })
        })
    });


    newCard.append(title, body, deadline, br, br2, btn);
    newCard.id = `task_${cards}`


    cardsContainer.prepend(newCard);

    const tosend = {
        name: name_inp.value,
        description: descrip.value,
        datetime: datetime.value
    };

    descrip.value = name_inp.value = datetime.value = ''

    requestAnimationFrame(() => {
        newCard.classList.remove('hidden')
    });

    fetch('/new_task', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(tosend)
    }).then(response => { return response.json(); })
        .then(data => { console.log(data); newCard['id'] = `task_${data["id"]}` });

}
// создание в живую

const log_enter = document.getElementById('log_enter');
const reg_enter = document.getElementById('reg_enter');
const logger = document.getElementById('logger');
const regger = document.getElementById('regger');
const reg_username = document.getElementById('reg_username');
const reg_pass = document.getElementById('reg_pass');
const log_username = document.getElementById('log_username');
const log_pass = document.getElementById('log_pass');
const sess_ok = document.getElementById('sess_ok');

log_enter.onclick = function () {
    log_enter.classList.add('none');
    reg_enter.classList.remove('none');
    regger.classList.add('none');
    logger.classList.remove('none');
}
reg_enter.onclick = function () {
    reg_enter.classList.add('none');
    log_enter.classList.remove('none');
    regger.classList.remove('none');
    logger.classList.add('none');
}
sess_ok.onclick = function () {
    if (!session_field.value || session_field.value.length > 36) { return }
    document.cookie = `sess_id=${session_field.value}; path=/; max-age=31536000`;
    alert('Сессия заменена');
    window.location.reload();

}
