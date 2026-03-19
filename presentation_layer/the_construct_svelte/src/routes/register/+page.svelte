<script lang="ts">
  import { goto } from '$app/navigation';
  import { authStore, isLoading, authError } from '$stores/auth';
  import Button from '$components/ui/Button.svelte';
  import Input from '$components/ui/Input.svelte';
  import Card from '$components/ui/Card.svelte';

  let email = '';
  let username = '';
  let password = '';
  let confirmPassword = '';
  let errors: Record<string, string> = {};

  function validateForm() {
    errors = {};
    if (!email) errors.email = 'Email is required';
    if (!username) errors.username = 'Username is required';
    if (password.length < 8) errors.password = 'Password must be at least 8 characters';
    if (password !== confirmPassword) errors.confirmPassword = 'Passwords do not match';
    return Object.keys(errors).length === 0;
  }

  async function handleRegister() {
    if (!validateForm()) {
      return;
    }

    try {
      await authStore.register({ email, username, password });
      goto('/profile');
    } catch (error) {
      console.error('Registration failed:', error);
    }
  }
</script>

<svelte:head>
  <title>Register - The Construct</title>
</svelte:head>

<div class="min-h-[80vh] flex items-center justify-center">
  <Card title="Create a new account" class="max-w-md w-full">
    <form on:submit|preventDefault={handleRegister} class="space-y-6">
      <Input
        label="Email"
        type="email"
        bind:value={email}
        error={errors.email || $authError || ''}
        required
      />
      <Input
        label="Username"
        type="text"
        bind:value={username}
        error={errors.username}
        required
      />
      <Input
        label="Password"
        type="password"
        bind:value={password}
        error={errors.password}
        required
      />
      <Input
        label="Confirm Password"
        type="password"
        bind:value={confirmPassword}
        error={errors.confirmPassword}
        required
      />
      <Button type="submit" variant="primary" fullWidth loading={$isLoading}>
        Create Account
      </Button>
    </form>
  </Card>
</div>
