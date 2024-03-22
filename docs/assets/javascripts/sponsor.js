document$.subscribe(() => {
    const html = `<hr><p style="text-align: center;"><a class="md-button" href="/#_4">赞助</a></p>`;

    if (window.location.hostname === "127.0.0.1" || window.location.pathname === '/') {
        return;
    }

    const comments = document.querySelector('#__comments');
    if (comments) {
        comments.insertAdjacentHTML('beforebegin', html);
    } else {
        const article = document.querySelector('article.md-typeset');
        article?.insertAdjacentHTML('beforeend', html);
    }
});
