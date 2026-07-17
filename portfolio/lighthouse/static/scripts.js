document.addEventListener('DOMContentLoaded', () => {
    initSearchPage();
    initBookDetailsPage();
    initAddBookPage();
})

/* Scripts for search.html */
function initSearchPage() {
    if (document.getElementById('book-results')) {
        const header = document.getElementById('site-header');
        const drawer = document.getElementById('drawer');
        const closeButton = document.getElementById('close-menu');
        const drawerToggle = document.getElementById('drawer-toggle');

        function adjustDrawerPosition() {
            const headerHeight = header.offsetHeight;
            drawer.style.top = `${headerHeight}px`;
            drawer.style.height = `calc(100% - ${headerHeight}px)`;
        }

        closeButton.addEventListener('click', () => {
            drawerToggle.checked = false;
        });

        window.addEventListener('load', adjustDrawerPosition);
        window.addEventListener('resize', adjustDrawerPosition);

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
