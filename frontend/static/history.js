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
    const token = localStorage.getItem('token'); // localStorage에서 데이터 가져오기
    const history_list_apiURL = `http://127.0.0.1:8000/history/list?token=${token}`;  // FastAPI 서버 URL
    const history_first_apiURL = `http://127.0.0.1:8000/history/list_first?token=${token}`;  // FastAPI 서버 URL

    function fetch_history_list() {
        fetch(history_list_apiURL, {
            method: "GET"
        }) 
            .then(response => response.json())
            .then(data => {
                const container = document.querySelector(".container");
                // container.innerHTML = "";  // Clear previous content

                data.forEach(item => {
                    console.log(item)   
                    const card = document.createElement("div");
                    card.className = `card card_list ${item.position_type}`;
                    
                    const enter_date = new Date(item.enter_time).toLocaleString();
                    const close_date = new Date(item.close_time).toLocaleString();

                    card.innerHTML = `
                        <div class="card-header">
                            <div>${item.symbol} <span class="${item.position_type}">${item.position_type}</span></div>
                            <div>
                                <span class="date">${enter_date}</span>
                                <span class="date">${close_date}</span>
                            </div>
                        </div>
                        <div class="card-content">
                            <div>진입 가격: ${item.entry_price}</div>
                            <div>평가손익: ${item.eval_PAL}</div>
                            <div>수익률: ${item.revenue_rate}%</div>
                            <div>매수 금액: ${item.purchase_price}</div>
                            <div>보유량: ${item.amount}</div>
                            <div>평가 금액: ${item.eval_price}</div>
                        </div>
                        <div class="card-footer">
                            <div>손절 금액: ${item.loss_end}</div>
                            <div>익절 금액: ${item.profit_end}</div>
                        </div>
                    `;
                    
                    container.appendChild(card);
                });
            });
    }

    function fetch_history_first() {
        fetch(history_first_apiURL, {
            method: "GET"
        }) 
            .then(response => response.json())
            .then(data => {
                const container = document.querySelector(".main_top");
                container.innerHTML = "";  // Clear previous content

                data.forEach(item => {
                    console.log("fist : ", item)
                    const card = document.createElement("div");
                    card.className = `card ${item.position_type}`;
                    
                    const enter_time = new Date(item.enter_time).toLocaleString();
                    const close_time = new Date(item.close_time).toLocaleString();

                    card.innerHTML = `
                        <div class="card-header">
                            <div>${item.symbol} <span class="${item.position_type}">${item.position_type}</span></div>
                            <div>
                                <span class="date">${enter_time}</span>
                                <span class="date">${close_time}</span>
                            </div>
                        </div>
                        <div class="card-content">
                            <div>진입 가격: ${item.entry_price}</div>
                            <div>평가손익: ${item.eval_PAL}</div>
                            <div>수익률: ${item.revenue_rate}%</div>
                            <div>매수 금액: ${item.purchase_price}</div>
                            <div>보유량: ${item.amount}</div>
                            <div>평가 금액: ${item.eval_price}</div>
                        </div>
                        <div class="card-footer">
                            <div>손절 금액: ${item.loss_end}</div>
                            <div>익절 금액: ${item.profit_end}</div>
                        </div>
                    `;
                    
                    container.appendChild(card);
                });
       
            });
    }

    loading_page(); // 로딩중 메시지 표시

    fetch_history_first();  // Initial fetch
    console.log("first");

    fetch_history_list();  // Initial fetch
    console.log("list");

    show_content(); 
    setInterval(fetch_history_first, 500);
});