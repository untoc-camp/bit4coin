function goTo(url) {
    const encoded = encodeURIComponent(url);
    window.location.href = `${encoded}.html`;
}

function loading_page() {
    document.getElementById("loading").style.display = "block";
    document.getElementById("content").style.display = "none";
}

function show_content() {
    document.getElementById("loading").style.display = "none";
    document.getElementById("content").style.display = "block";
}

document.addEventListener("DOMContentLoaded", function() {
    const symbol_apiURL = "http://127.0.0.1:8000/symbols/symbols_info"; // FastAPI 서버 URL
    function loading() {
        loading_page(); // 로딩중 메시지 표시
    }

    function fetch_symbol() {
        fetch(symbol_apiURL)
            .then(response => response.json())
            .then(data => {
                console.log(data);
                const table = document.getElementById("symbol_prices");
                table.innerHTML = ""; // Clear previous content
                const symbols = ["ETH", "BTC", "XRP", "DOGE", "SOL", "STX", "BNB", "TRX", "LINK", "NEO", "SXP", "ATOM", "XLM", "KAS", "TON"]; // symbol 추가 = > home.symbols_info에도 추가하기

                symbols.forEach(symbol => {
                    const row = document.createElement("tr");
                    const symbol_cell = document.createElement("td");
                    symbol_cell.textContent = symbol;

                    const price_cell = document.createElement("td");
                    price_cell.textContent = `${data[symbol + '_cur_price']}$`;

                    const time_percent_change = document.createElement("td");
                    const change_value = data[symbol + '_daily_per'];
                    time_percent_change.textContent = `${change_value}%`;

                    if (change_value > 0) {
                        time_percent_change.classList.add("positive");
                    } else if (change_value < 0) {
                        time_percent_change.classList.add("negative");
                    } else {
                        time_percent_change.classList.add("neutral");
                    }

                    row.appendChild(symbol_cell);
                    row.appendChild(price_cell);
                    row.appendChild(time_percent_change);
                    table.appendChild(row);
                });
                show_content(); // 데이터 로드 후 로딩중 메시지 숨기기
            })
            .catch(error => {
                console.error("Error fetching data: ", error);
                // 에러 발생 시 로딩중 메시지를 숨기지 않도록 할 수 있음
            });
    }

    loading();
    fetch_symbol();
    try {
        setInterval(fetch_symbol, 500);
        console.log("good work");
    } catch (e) {
        console.log(e);
        // alert(`다음과 같은 에러가 발생했습니다: ${e.name}: ${e.message}`);
    }
});
