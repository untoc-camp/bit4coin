function goTo(url) {
    const encoded = encodeURIComponent(url);
    window.location.href = `/backend_copy/templates/${encoded}.html`;
}     