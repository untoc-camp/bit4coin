function goTo(url) {
    const encoded = encodeURIComponent(url);
    window.location.href = `${encoded}.html`;
}