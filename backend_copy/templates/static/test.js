document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("balance_form").addEventListener("submit", function(event) {
        event.preventDefault();
        axios.post('/balance')
            .then(function(response) {
                document.getElementById("balance").innerHTML = response.data;
            })
            .catch(function(error) {
                console.error("There was an error retrieving the balance!", error);
            });
    });

    document.getElementById("curPrice_form").addEventListener("submit", function(event) {
        event.preventDefault();
        const coinName = document.getElementById("symbol").value;
        const formData = new FormData();
        formData.append("symbol", coinName);

        axios.post('/cur_price', formData)
            .then(function(response) {
                document.getElementById("cur_price").innerHTML = response.data;
            })
            .catch(function(error) {
                console.error("There was an error retrieving the current price!", error);
            });
    });

});
