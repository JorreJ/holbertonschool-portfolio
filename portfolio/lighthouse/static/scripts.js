document.addEventListener('DOMContentLoaded', () => {
    initSearchPage();
    initBookDetailsPage();
    initAddBookPage();
    initTomSelect();
});

/* Scripts for search.html */
function initSearchPage() {
    if (document.getElementById('book-results')) {
        const header = document.getElementById('site-header');
        const drawer = document.getElementById('drawer');
        const closeButton = document.getElementById('close-menu');
        const drawerToggle = document.getElementById('drawer-toggle');
        const drawerButton = document.getElementById('drawer-button')

        function adjustDrawerPosition() {
            const headerHeight = header.offsetHeight;

            if (window.scrollY < headerHeight) {
                drawer.style.top = `${headerHeight}px`;
                drawer.style.height = `calc(100vh - ${headerHeight}px)`;
                drawerButton.style.top = `${headerHeight + 10}px`;
            } else {
                drawer.style.top = "0px";
                drawer.style.height = `calc(100vh)`;
                drawerButton.style.top = "10px";
            }
        }

        closeButton.addEventListener('click', () => {
            drawerToggle.checked = false;
        });

        window.addEventListener('load', adjustDrawerPosition);
        window.addEventListener('resize', adjustDrawerPosition);
        window.addEventListener('scroll', adjustDrawerPosition);

        document.getElementById('search-form').addEventListener('submit', function(e) {
            e.preventDefault();

            const form = e.target;
            const formData = new FormData(form);
            const params = new URLSearchParams(formData).toString();

            fetch(`?${params}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.text())
            .then(html => {
                document.getElementById('book-results').innerHTML = html;
            });
        });
    }
}

/* Script for book_details.html */
function initBookDetailsPage() {
    if (document.getElementById('bookDetailsPage')) {
        document.getElementById('openBorrowPopup').addEventListener('click', function() {
            document.getElementById('borrowPopup').classList.remove('hidden');
        });

        document.getElementById('cancel-button').addEventListener('click', function () {
            document.getElementById('borrowPopup').classList.add('hidden');
        });

        document.getElementById('borrow-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const borrower = document.getElementById('borrower').value;
            const borrowButton = document.getElementById('openBorrowPopup');
            const borrowUrl = borrowButton.dataset.url;
            const csrfToken = borrowButton.dataset.csrf;

            fetch(borrowUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ borrower: borrower })
            })
            .then(response => response.json())
            .then(data =>  {
                alert(data.message);
                document.getElementById('borrowPopup').classList.add('hidden');
            });
        });
    }
}

function fillField(id, value) {
    const field = document.getElementById(id);

    if (field && value) {
        field.value = value;
    }
}

/* Script for add_book.html */
function initAddBookPage() {
    const isbnInput = document.getElementById('isbn-input');
    if (!isbnInput) {
        return;
    }
    isbnInput.addEventListener('change', function () {
        const isbn = isbnInput.value.trim();
        if (isbn.length < 10) {
            return;
        }

        fetch(`/books/search-isbn/?isbn=${isbn}`)
        .then(response => response.json())
        .then(data => {

            console.log("Données reçues :", data);

            fillField('title-input', data.title);
            fillField('author-input', data.author);
            fillField('published-input', data.published);
            fillField('edition-input', data.edition);
            fillField('summary-input', data.summary);
            fillField('language-input', data.language);
            fillField('cover-input', data.cover)
        })
        .catch(error => {
            console.error("Erreur recherche ISBN :", error);
        });
    });
}

function initTomSelect(){
    const category = document.getElementById("category-input");
    if (!category) {
        return;
    }

    new TomSelect(category, {
        plugins: ['remove_button'],
        maxItems: null,
        persist: false,
        createOnBlur: true,
        sortField: {
            field: "text",
            direction: "asc"
        },
        create: function(input, callback) {
            fetch("/categories/create/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": getCookie("csrftoken")
                },

                body: new URLSearchParams({
                    name: input
                })
            })

            .then(response => response.json())
            .then(data => {
                callback({
                    value: data.id,
                    text: data.name
                });
            })

            .catch(() => callback());
        }
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
