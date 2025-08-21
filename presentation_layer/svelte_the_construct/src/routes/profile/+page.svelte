<script lang="ts">
  import { onMount } from 'svelte';
  import { goto } from '$app/navigation';
  import { user, isAuthenticated, authStore } from '$stores/auth';
  import Button from '$components/ui/Button.svelte';
  import Card from '$components/ui/Card.svelte';
  import Input from '$components/ui/Input.svelte';

  let isEditing = false;
  let profileData: any = {};

  onMount(() => {
    if (!$isAuthenticated) {
      goto('/login?redirect=/profile');
    } else {
      profileData = { ...$user?.profile };
    }
  });

  async function handleUpdateProfile() {
    try {
      await authStore.updateProfile({ profile: profileData });
      isEditing = false;
    } catch (error) {
      console.error('Failed to update profile:', error);
    }
  }
</script>

<svelte:head>
  <title>My Profile - The Construct</title>
</svelte:head>

<div class="profile-page max-w-4xl mx-auto">
  <div class="flex justify-between items-center mb-8">
    <h1 class="text-4xl font-bold">My Profile</h1>
    <Button variant="outline" on:click={() => isEditing = !isEditing}>
      {isEditing ? 'Cancel' : 'Edit Profile'}
    </Button>
  </div>

  {#if $user}
    <Card>
      {#if isEditing}
        <form on:submit|preventDefault={handleUpdateProfile} class="space-y-6">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Input label="First Name" bind:value={profileData.first_name} />
            <Input label="Last Name" bind:value={profileData.last_name} />
          </div>
          <Input label="Avatar URL" bind:value={profileData.avatar} />
          <Input label="Bio" bind:value={profileData.bio} />
          <div class="flex justify-end gap-4">
            <Button type="button" variant="ghost" on:click={() => isEditing = false}>
              Cancel
            </Button>
            <Button type="submit" variant="primary">
              Save Changes
            </Button>
          </div>
        </form>
      {:else}
        <div class="space-y-6">
          <div class="flex items-center gap-6">
            <div class="avatar">
              <div class="w-24 rounded-full ring ring-primary ring-offset-base-100 ring-offset-2">
                <img src={profileData.avatar || `https://i.pravatar.cc/150?u=${$user.id}`} alt="User avatar" />
              </div>
            </div>
            <div>
              <h2 class="text-2xl font-bold">{$user.username}</h2>
              <p class="text-base-content/70">{$user.email}</p>
            </div>
          </div>
          <div class="divider"></div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div class="text-sm text-base-content/70">First Name</div>
              <div class="text-lg font-medium">{profileData.first_name || 'N/A'}</div>
            </div>
            <div>
              <div class="text-sm text-base-content/70">Last Name</div>
              <div class="text-lg font-medium">{profileData.last_name || 'N/A'}</div>
            </div>
          </div>
          <div>
            <div class="text-sm text-base-content/70">Bio</div>
            <p>{profileData.bio || 'No bio provided.'}</p>
          </div>
        </div>
      {/if}
    </Card>
  {/if}
</div>
