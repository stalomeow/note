document$.subscribe(() => {
    const html = `<br><p style="text-align: center;"><a class="md-button" href="https://stalomeow.com/#coffee" target="_blank">赞助</a></p>`;

    if (window.location.hostname === "127.0.0.1") {
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
