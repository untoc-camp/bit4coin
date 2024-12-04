function goTo(url) {
    const encoded = encodeURIComponent(url);
    window.location.href = `/backend_copy/templates/${encoded}.html`;
}


document.addEventListener("DOMContentLoaded", function() {
    const apiURL = "http://127.0.0.1:8000/symbols_info";  // FastAPI 서버 URL

    function fetchData() {
        fetch(apiURL)
            .then(response => response.json())
            .then(data => {
                const tbody = document.getElementById("crypto-prices");
                tbody.innerHTML = "";  // Clear previous content
                const cryptos = ["ETH", "BTC", "XRP", "DOGE", "SOL", "STX"];

                cryptos.forEach(crypto => {
                    const row = document.createElement("tr");

                    const symbolCell = document.createElement("td");
                    symbolCell.textContent = cryptoNames(crypto);

                    const priceCell = document.createElement("td");
                    priceCell.textContent = `${data[crypto + '_cur_price']}$`;

                    const changeCell = document.createElement("td");
                    const changeValue = data[crypto + '_daily_per'];
                    changeCell.textContent = `${changeValue}%`;

                    if (changeValue > 0) {
                        changeCell.classList.add("positive");
                    } else if (changeValue < 0) {
                        changeCell.classList.add("negative");
                    } else {
                        changeCell.classList.add("neutral");
                    }

                    row.appendChild(symbolCell);
                    row.appendChild(priceCell);
                    row.appendChild(changeCell);
                    tbody.appendChild(row);
                });
            });
    }

    function cryptoNames(symbol) {
        const names = {
            "ETH": "ETH",
            "BTC": "BTC",
            "XRP": "XRP",
            "DOGE": "DOGE",
            "SOL": "SOL",
            "STX": "STX"
        };
        return names[symbol];
    }

    fetchData();  // Initial fetch
    setInterval(fetchData, 1000);  // Fetch every 1 second
});