function goTo(url) {
    const encoded = encodeURIComponent(url);
    window.location.href = `/${encoded}`;
}
function goToBack() {
    window.history.back();
}
