function fillFilmList() {
    fetch('/lab7/rest-api/films/')
        .then(response => response.json())
        .then(films => {
            let tbody = document.getElementById('film-list');
            tbody.innerHTML = '';

            for (let i = 0; i < films.length; i++) {
                let tr = document.createElement('tr');

                let tdTitleRus = document.createElement('td');
                let tdTitle = document.createElement('td');
                let tdYear = document.createElement('td');
                let tdDescription = document.createElement('td');
                let tdActions = document.createElement('td');

                // Заполнение данных
                tdTitleRus.innerText = films[i].title_ru;
                tdTitle.innerHTML = films[i].title ? `<em>(${films[i].title})</em>` : ''; // Оригинальное название курсивом
                tdYear.innerText = films[i].year;
                tdDescription.innerText = films[i].description;

                // Кнопка редактирования
                let editButton = document.createElement('button');
                editButton.innerText = 'Редактировать';
                editButton.onclick = () => editFilm(i);

                // Кнопка удаления
                let delButton = document.createElement('button');
                delButton.innerText = 'Удалить';
                delButton.onclick = () => deleteFilm(i, films[i].title_ru);

                // Добавляем кнопки в ячейку действий
                tdActions.append(editButton);
                tdActions.append(delButton);

                // Добавляем ячейки в строку
                tr.append(tdTitleRus);
                tr.append(tdTitle);
                tr.append(tdYear);
                tr.append(tdDescription);
                tr.append(tdActions);

                // Добавляем строку в таблицу
                tbody.append(tr);
            }
        })
        .catch(error => console.error('Ошибка при загрузке фильмов:', error));
}

function deleteFilm(id, title) {
    if (!confirm(`Вы точно хотите удалить фильм "${title}"?`)) return;

    fetch(`/lab7/rest-api/films/${id}`, { method: 'DELETE' })
        .then(() => fillFilmList())
        .catch(error => console.error('Ошибка при удалении фильма:', error));
}

function sendFilm() {
    const id = document.getElementById('id').value;
    const film = {
        title: document.getElementById('title').value,
        title_ru: document.getElementById('title-ru').value,
        year: parseInt(document.getElementById('year').value), // Преобразование в число
        description: document.getElementById('description').value
    };

    const url = id === '' ? '/lab7/rest-api/films/' : `/lab7/rest-api/films/${id}`;
    const method = id === '' ? 'POST' : 'PUT';

    fetch(url, {
        method: method,
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(film)
    })
    .then(response => {
        if (response.ok) {
            fillFilmList();
            hideModal();
            return {};
        }
        return response.json();
    })
    .then(errors => {
        // Очистка предыдущих ошибок
        document.getElementById('title-error').innerText = '';
        document.getElementById('title-ru-error').innerText = '';
        document.getElementById('year-error').innerText = '';
        document.getElementById('description-error').innerText = '';

        // Вывод ошибок из сервера
        if (errors.title) document.getElementById('title-error').innerText = errors.title;
        if (errors.title_ru) document.getElementById('title-ru-error').innerText = errors.title_ru;
        if (errors.year) document.getElementById('year-error').innerText = errors.year;
        if (errors.description) document.getElementById('description-error').innerText = errors.description;
    })
    .catch(error => console.error('Ошибка при отправке данных фильма:', error));
}

function editFilm(id) {
    fetch(`/lab7/rest-api/films/${id}`)
        .then(response => response.json())
        .then(film => {
            document.getElementById('id').value = id;
            document.getElementById('title').value = film.title;
            document.getElementById('title-ru').value = film.title_ru;
            document.getElementById('year').value = film.year;
            document.getElementById('description').value = film.description;

            // Очистка ошибок при открытии формы
            clearErrors();
            showModal();
        })
        .catch(error => console.error('Ошибка при загрузке фильма для редактирования:', error));
}

function showModal() {
    document.querySelector('div.modal').style.display = 'block';
    clearErrors(); // Очистка ошибок при открытии модального окна
}

function hideModal() {
    document.querySelector('div.modal').style.display = 'none';
}

function cancel() {
    hideModal();
}

function addFilm() {
    document.getElementById('id').value = '';
    document.getElementById('title').value = '';
    document.getElementById('title-ru').value = '';
    document.getElementById('year').value = '';
    document.getElementById('description').value = '';

    clearErrors();
    showModal();
}

function clearErrors() {
    document.getElementById('title-error').innerText = '';
    document.getElementById('title-ru-error').innerText = '';
    document.getElementById('year-error').innerText = '';
    document.getElementById('description-error').innerText = '';
}