document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('profileForm').addEventListener('submit', function (event) {
        event.preventDefault();
        validateProfileForm();
    });
});


document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('askForm').addEventListener('submit', function (event) {
        event.preventDefault();
        validateAskForm();
    });
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('authForm').addEventListener('submit', function (event) {
        event.preventDefault();
        validateAuthForm();
    });
});

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('regForm').addEventListener('submit', function (event) {
        event.preventDefault();
        validateRegForm();
    });
});


function validateProfileForm() {
    // Login
    var loginInput = document.getElementById('loginInput').value;
    var loginRow = document.getElementById('loginRow');

    // if (loginInput.trim() === 'login8') {
    //     loginRow.insertAdjacentHTML('afterbegin',
    //         '<div class="warning-card-body p-1 mb-3">Sorry, this login already in use!</div>');
    // }

    // Очищаем предупреждения перед добавлением новых
    loginRow.innerHTML = '';


    if (loginInput.trim() === '') {
        loginRow.insertAdjacentHTML('afterbegin',
            '<div class="warning-card-body p-1 mb-3">Sorry, but the login is missing!</div>');
    }

    if (loginInput.trim().length > 20) {
        loginRow.insertAdjacentHTML('afterbegin',
            '<div class="warning-card-body p-1 mb-3">Sorry, but the max size of the login is 20 symbols!</div>');
    }

    // Email
    var emailInput = document.getElementById('emailInput').value;
    var emailRow = document.getElementById('emailRow');

    // Очищаем предупреждения перед добавлением новых
    emailRow.innerHTML = '';

    if (emailInput.trim() === '') {
        emailRow.insertAdjacentHTML('afterbegin',
            '<div class="warning-card-body p-1 mb-3">Sorry, this email address already in use!</div>');
    }

    // Avatar
    // var avatarInput = document.getElementById('avatarInput').value;
    // var avatarRow = document.getElementById('avatarRow');
    //
    // if (avatarInput.trim() === '') {
    //     avatarRow.insertAdjacentHTML('afterbegin',
    //         '<div class="warning-card-body p-1 mb-3">Wrong format of the file or too big size!</div>');
    // }
}


function validateAskForm() {
    // Title
    var titleInput = document.getElementById('titleInput').value;
    var titleRow = document.getElementById('titleRow');

    // Очищаем предупреждения перед добавлением новых
    titleRow.innerHTML = '';

    if (titleInput.trim() === '') {
        titleRow.insertAdjacentHTML('afterbegin',
            '<div class="card mt-3">\n' +
            '                <div class="card-body warning-card-body">\n' +
            '                    Title is missing\n' +
            '                </div>\n' +
            '            </div>');
    }

    // Body
    var bodyInput = document.getElementById('bodyInput').value;
    var bodyRow = document.getElementById('bodyRow');

    // Очищаем предупреждения перед добавлением новых
    bodyRow.innerHTML = '';

    if (bodyInput.trim().length < 20) {
        bodyRow.insertAdjacentHTML('afterbegin',
            '<div class="card mt-3">\n' +
            '          <div class="card-body warning-card-body">\n' +
            '                Minimum 20 symbols\n' +
            '          </div>\n' +
            '     </div>');
    }


    // Body
    var tagInput = document.getElementById('tagInput').value;
    var tagRow = document.getElementById('tagRow');

    // Очищаем предупреждения перед добавлением новых
    tagRow.innerHTML = '';

    if (!IsMaxThreeTags(tagInput.trim()) && tagInput.trim() !== '') {
        tagRow.insertAdjacentHTML('afterbegin',
            '<div class="card mt-3">\n' +
            '           <div class="card-body warning-card-body">\n' +
            '               Maximum 3 tags\n' +
            '           </div>\n' +
            '    </div>');
    }

}

// незавершенная проверка через регулярку
function IsMaxThreeTags(input) {
    // Регулярное выражение для проверки формата ввода
    var regex = /^\s*[\w\s]+(?:,\s*[\w\s]+){0,2}\s*$/;

    // Проверка совпадения с регулярным выражением
    return regex.test(input);
}


function validateAuthForm() {
    // Title
    var loginInput = document.getElementById('loginInput').value;
    var passInput = document.getElementById('passInput').value;
    var authRow = document.getElementById('authRow');

    // Очищаем предупреждения перед добавлением новых
    authRow.innerHTML = '';

    if (loginInput.trim() === '' || passInput.trim() === '') {
        authRow.insertAdjacentHTML('afterbegin',
            '<div class="card my-3 d-inline-flex">\n' +
            '        <div class="card-body warning-card-body">\n' +
            '            Sorry, wrong password or login!\n' +
            '        </div>\n' +
            '    </div>');
    }
}


function validateRegForm() {
    // Title
    var loginInput = document.getElementById('loginInput').value;
    var loginRow = document.getElementById('loginRow');

    // Очищаем предупреждения перед добавлением новых
    loginRow.innerHTML = '';

    if (loginInput.trim() === '') {
        loginRow.insertAdjacentHTML('afterbegin',
            '<div class="warning-card-body p-1 my-3">\n' +
            '            Sorry, this login already in use!\n' +
            '        </div>');
    }

    if (loginInput.trim().length > 20) {
        loginRow.insertAdjacentHTML('afterbegin',
            '<div class="warning-card-body p-1 my-3">\n' +
            '            Sorry, but the max size of the login is 20 symbols! \n' +
            '        </div>');
    }

    var emailInput = document.getElementById('emailInput').value;
    var emailRow = document.getElementById('emailRow');

    // Очищаем предупреждения перед добавлением новых
    emailRow.innerHTML = '';

    if (emailInput.trim() === '') {
        loginRow.insertAdjacentHTML('afterbegin',
            '<div class="warning-card-body p-1 my-3">\n' +
            '            Sorry, this email address already in use!\n' +
            '        </div>');
    }

    // var avatarInput = document.getElementById('avatarInput').value;
    // var avatarRow = document.getElementById('avatarRow');
    //
    //  // Очищаем предупреждения перед добавлением новых
    // avatarRow.innerHTML = '';
    //
    // if (avatarInput.trim() === '') {
    //     avatarRow.insertAdjacentHTML('afterbegin',
    //         '<div class="warning-card-body p-1 my-3">\n' +
    //         '            Wrong format of the file or too big size!\n' +
    //         '        </div>');
    // }

    var passInput = document.getElementById('passInput').value;
    var passInputRepeat = document.getElementById('passInputRepeat').value;
    var passRow = document.getElementById('passRow');

    // Очищаем предупреждения перед добавлением новых
    passRow.innerHTML = '';

    if ((passInput.trim() !== passInputRepeat.trim()) || (passInput.trim() === '' && passInputRepeat.trim() === '')) {
        passRow.insertAdjacentHTML('afterbegin',
            '<div class="warning-card-body p-1 my-3">\n' +
            '            Password mismatch!\n' +
            '        </div>');
    }

}