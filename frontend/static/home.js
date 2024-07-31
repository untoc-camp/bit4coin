
function goTo(url) {
    const encoded = encodeURIComponent(url);
    window.location.href = `${encoded}.html`;}

document.addEventListener("DOMContentLoaded", function() {
    // 전략선택시 간단하게 설명해주는 desc
    function update_description() {
        const symbol = document.getElementById('symbol').value;
        const purchase_percent = document.getElementById('purchase_percent').value;
        const leverage = document.getElementById('leverage').value;
        const strategy = document.getElementById('strategy').value;

        let strategy_desc = '';
        if (strategy === 'strategy_1') {
            strategy_desc = `
                <p style="font-weight:bold">${symbol}</p>
                <p>purchase percent : ${purchase_percent*100}%</p>
                <p>leverage : ${leverage}배</p>
                <p>profit percent : 0.8%</p>
                <p>loss percent : 1.6%</p>
                <p>timeframe : 15m</p>
                <p>변동성 돌파전략과 SMA를 사용</p>
            `;
        } else if (strategy === 'strategy_2') {
            strategy_desc = `
                <p style="font-weight:bold">${symbol}</p>
                <p>purchase percent : ${purchase_percent*100}%</p>
                <p>leverage : ${leverage}배</p>
                <p>profit percent : 0.8%</p>
                <p>loss percent : 1.6%</p>
                <p>timeframe : 30m</p>
                <p>변동성 돌파전략과 SMA를 사용</p>
            `;
        } else if (strategy === 'strategy_3') {
            strategy_desc = `
                <p style="font-weight:bold">${symbol}</p>
                <p>purchase percent : ${purchase_percent*100}%</p>
                <p>leverage : ${leverage}배</p>
                <p>profit percent : 2%</p>
                <p>loss percent : 4%</p>
                <p>timeframe : 1d</p>
                <p>변동성 돌파전략과 SMA를 사용</p>
            `;
        }

        // desciption의 내용 : brief
        descriptions = document.getElementById('description')
        descriptions.style.display = "block"
        descriptions.innerHTML = strategy_desc;

        // modal의 내용 : detail
        modal_desc = strategy_desc + "디테일한 내용 추가하기!!"
        document.getElementById("modal_des").innerHTML = modal_desc;

        // 전략과 코인을 보여주는 내용 : strategy - symbol
        ss = `${strategy}  ${symbol} 거래중` 
        localStorage.setItem('strategySymbol', ss);  
        saved_strategy_symbol = localStorage.getItem('strategySymbol')
        document.getElementById("strategy-symbol").textContent = saved_strategy_symbol;
    }

    document.getElementById('strategy').addEventListener('change', update_description);
});



document.addEventListener("DOMContentLoaded", function() {
    // 디테일 모달
    const modal = document.querySelector('.modal_detail');
    const modalOpen = document.querySelector('#enter');
    const modalClose = document.querySelector('#close_detail');

    // 전략과 코인 알려주는 모달
    const modal_in_position = document.querySelector('.modal_in_position'); 
    const yes_button = document.getElementById("enter_position");   
    const end_button = document.getElementById('stop_position');

    
    // 페이지 로드 시 상태를 로드하여 모달의 상태를 설정
    const modal_in_position_state = localStorage.getItem('modal_in_position_state');
    const savedTaskId = localStorage.getItem('task_id');
    const saved_strategy_symbol = localStorage.getItem("strategySymbol")
    if (modal_in_position_state === 'block' && savedTaskId && saved_strategy_symbol) {
        modal_in_position.style.display = 'block';
        end_button.setAttribute('data_task_id', savedTaskId);
        document.getElementById("strategy-symbol").textContent = saved_strategy_symbol;
    }

    // 거래 진입 모달 페이지 띄우기
    modalOpen.addEventListener('click', function(){
        modal.style.display = 'block';
    });

    // 거래 진입 보달 페이지 내리기
    modalClose.addEventListener('click', function(){
       // Hide modal
        modal.style.display = 'none';
    });

    // 포지션에 진입한함-> 전략과 코인의 정보를 알려주는 모달페이지
    yes_button.addEventListener('click', function() {



        const form = document.getElementById('enter_position_form');
        const formData = new FormData(form);
        const jsonData = {};
        formData.forEach((value, key) => {
                jsonData[key] = value;
            });

        // 포지션 진입
        fetch("http://127.0.0.1:8000/enter_position", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(jsonData),
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                const stopPosition = document.getElementById('stop_position');
                stopPosition.setAttribute('data_task_id', data.task_id);
                localStorage.setItem('task_id', data.task_id);  
            })
            .catch(error => {
                console.error('Error:', error);
            });
        modal.style.display = 'none';
            
        modal_in_position.style.display = 'block';
        localStorage.setItem('modal_in_position_state', 'block'); // 상태 저장

    });

    // 전략과 코인의 정보를 알려주는 모달페이지를 닫고 백그라운드 실행을 멈춤
    end_button.addEventListener('click', function(){
        var taskId = this.getAttribute("data_task_id");
        console.log("task_id is", taskId)
        modal_in_position.style.display = 'none';
        localStorage.setItem('modal_in_position_state', 'none');

        localStorage.removeItem('strategySymbol');


        // 포지션 나가기
        fetch(`http://127.0.0.1:8000/stop_position?task_id=${taskId}`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data)
            if (data.message) {
                localStorage.removeItem('task_id');
                alert("작업이 성공적으로 중지되었습니다.");
            } else {
                alert("작업 중지에 실패했습니다.");
            }
        })
        .catch(error => {
            console.error("Error stopping the task:", error);
            alert("작업 중지 중 오류가 발생했습니다.");
        });
    });

});
