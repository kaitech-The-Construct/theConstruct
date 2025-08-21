<script lang="ts">
  import { goto } from '$app/navigation';
  import { authStore, isLoading, authError } from '$stores/auth';
  import Button from '$components/ui/Button.svelte';
  import Input from '$components/ui/Input.svelte';
  import Card from '$components/ui/Card.svelte';

  let email = '';
  let password = '';

  async function handleLogin() {
    try {
      await authStore.login({ username: email, password });
      goto('/profile');
    } catch (error) {
      console.error('Login failed:', error);
    }
  }
</script>

<svelte:head>
  <title>Login - The Construct</title>
</svelte:head>

<div class="min-h-[80vh] flex items-center justify-center">
  <Card title="Login to your account" class="max-w-md w-full">
    <form on:submit|preventDefault={handleLogin} class="space-y-6">
      <Input
        label="Email"
        type="email"
        bind:value={email}
        error={$authError || ''}
        required
      />
      <Input
        label="Password"
        type="password"
        bind:value={password}
        required
      />
      <Button type="submit" variant="primary" fullWidth loading={$isLoading}>
        Login
      </Button>
    </form>
  </Card>
</div>
