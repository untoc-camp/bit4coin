<script>
  let item_list = []

  function get_item_list() {
    fetch("http://127.0.0.1:8000/history/item").then((response) => {
      response.json().then((json) => {
        item_list = json
      })
    })
  }

  get_item_list()
</script>

<ul>
  {#each item_list as item}
    <li>{item}</li>
  {/each}
</ul>
