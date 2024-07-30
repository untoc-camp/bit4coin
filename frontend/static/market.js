

function filterMarkets() {
    const searchInput = document.getElementById('search').value.toLowerCase();
    const marketItems = document.getElementsByClassName('market-item');
    
    for (let i = 0; i < marketItems.length; i++) {
        const market = marketItems[i].textContent.toLowerCase();
        if (market.includes(searchInput)) {
            marketItems[i].style.display = 'flex';
        } else {
            marketItems[i].style.display = 'none';
        }
    }
}
function goToMarket(market) {
    window.location.href = `/markets/${market}`;
}