
function goTo(url) {
    const encoded = encodeURIComponent(url);
    window.location.href = `/backend_copy/templates/${encoded}.html`;
}

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
        document.getElementById('description').innerHTML = strategy_desc;

        // modal의 내용 : detail
        modal_desc = strategy_desc + "디테일한 내용 추가하기!!"
        document.getElementById("modal_des").innerHTML = modal_desc;
    }

    document.getElementById('strategy').addEventListener('change', update_description);
});



document.addEventListener("DOMContentLoaded", function() {
    const modal = document.querySelector('.modal_detail');
    const modalOpen = document.querySelector('#enter');
    const modalClose = document.querySelector('#close_detail');

    // Open modal when the button is clicked
    modalOpen.addEventListener('click', function(){
        // Display modal
        modal.style.display = 'block';
    });

    // Close modal when the close button is clicked
    modalClose.addEventListener('click', function(){
       // Hide modal
        modal.style.display = 'none';
    });

    // Submit form when the Yes button is clicked
     const yesButton = document.querySelector('#enter_position');
    yesButton.addEventListener('click', function() {
        const form = document.getElementById('enter_position_form');
        const formData = new FormData(form);
        const jsonData = {};
        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

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

            modal.style.display = 'none'; // Close modal after submission
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

});