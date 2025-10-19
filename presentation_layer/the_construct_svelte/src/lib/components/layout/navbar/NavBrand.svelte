<script lang="ts">
  import { goto } from '$app/navigation';
  
  function handleClick() {
    goto('/');
  }
</script>

<button 
  class="nav-brand"
  on:click={handleClick}
  aria-label="Go to homepage"
>
  <span class="brand-the">The</span>
  <span class="brand-construct">Construct</span>
</button>
