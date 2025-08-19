<script>
  let count = 0;
  const increment = () => {
    count += 1;
  };
</script>

<main>
  <h1>The Construct</h1>
  <p>Presentation Layer (Svelte)</p>

  <div class="card">
    <button on:click={increment}>
      count is {count}
    </button>
  </div>
</main>

<style>
  :root {
    font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
    line-height: 1.5;
    font-weight: 400;
    color-scheme: light dark;
    color: rgba(255, 255, 255, 0.87);
    background-color: #242424;
  }
  main {
    text-align: center;
    padding: 1em;
    margin: 0 auto;
  }
</style>
