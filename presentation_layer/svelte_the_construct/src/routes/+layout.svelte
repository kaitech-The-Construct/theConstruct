<script>
  import Header from '$lib/components/layout/Header.svelte';
  import '../app.css'; // Assuming a global stylesheet
</script>

<Header />

<main>
  <slot></slot>
</main>

<style>
  main {
    padding: 2rem;
  }
</style>
