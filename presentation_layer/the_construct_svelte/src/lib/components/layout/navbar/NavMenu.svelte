<script lang="ts">
  export let currentPath: string;
  
  const navItems = [
    { href: '/', label: 'Home' },
    { href: '/marketplace', label: 'Marketplace' },
    { href: '/manufacturing', label: 'Manufacturing' },
    { href: '/about', label: 'About' }
  ];
</script>

<nav class="nav-menu" role="navigation" aria-label="Main navigation">
  {#each navItems as item}
    <a 
      href={item.href}
      class="nav-item"
      class:active={currentPath === item.href}
      aria-current={currentPath === item.href ? 'page' : undefined}
    >
      {item.label}
    </a>
  {/each}
</nav>
