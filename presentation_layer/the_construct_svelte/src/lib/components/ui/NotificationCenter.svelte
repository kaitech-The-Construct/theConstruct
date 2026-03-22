<script lang="ts">
  import { notificationStore } from '$stores/notifications';
  import { fade, slide } from 'svelte/transition';

  let isOpen = false;

  function toggleDropdown() {
    isOpen = !isOpen;
  }

  function handleMarkAsRead(id: string | undefined) {
    if (!id) return;
    notificationStore.markAsRead(id);
  }

  function handleDismissAlert(id: string | undefined) {
    if (!id) return;
    notificationStore.dismissAlert(id);
  }
  
  // Close when clicking outside
  function handleClickOutside(event: MouseEvent) {
    const target = event.target as HTMLElement;
    if (isOpen && !target.closest('.notification-container')) {
      isOpen = false;
    }
  }

  import { onMount, onDestroy } from 'svelte';

  onMount(() => {
    document.addEventListener('click', handleClickOutside);
  });

  onDestroy(() => {
    document.removeEventListener('click', handleClickOutside);
  });
</script>

<div class="notification-container relative inline-block">
  <button
    class="btn btn-ghost btn-circle relative"
    onclick={toggleDropdown}
    aria-label="Notifications"
  >
    <svg
      xmlns="http://www.w3.org/2000/svg"
      class="h-5 w-5"
      fill="none"
      viewBox="0 0 24 24"
      stroke="currentColor"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
      />
    </svg>
    {#if $notificationStore.unreadCount > 0}
      <span class="badge badge-sm badge-secondary absolute top-0 right-0">
        {$notificationStore.unreadCount}
      </span>
    {/if}
  </button>

  {#if isOpen}
    <div 
      transition:fade={{ duration: 150 }}
      class="absolute right-0 mt-2 w-80 sm:w-96 bg-base-100 rounded-box shadow-xl border border-base-300 z-50 overflow-hidden flex flex-col max-h-[80vh]"
    >
      <div class="p-4 border-b border-base-200 bg-base-200/50 flex justify-between items-center">
        <h3 class="font-bold text-lg">Notifications</h3>
        {#if $notificationStore.unreadCount > 0}
          <span class="text-xs text-base-content/60">
            {$notificationStore.unreadCount} unread
          </span>
        {/if}
      </div>

      <div class="overflow-y-auto flex-1 p-2 space-y-2">
        <!-- Active Alerts Section -->
        {#if $notificationStore.activeAlerts.length > 0}
          <div class="px-2 pt-2 pb-1 text-xs font-semibold text-base-content/50 uppercase tracking-wider">
            System Alerts
          </div>
          {#each $notificationStore.activeAlerts as alert (alert.alert_id || alert.id)}
            <div transition:slide={{ duration: 200 }} class="p-3 bg-error/10 border border-error/20 rounded-lg relative group">
              <button 
                class="absolute top-2 right-2 text-error/50 hover:text-error opacity-0 group-hover:opacity-100 transition-opacity"
                onclick={() => handleDismissAlert(alert.alert_id || alert.id)}
                aria-label="Dismiss alert"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" /></svg>
              </button>
              <h4 class="font-bold text-sm text-error flex items-center gap-1">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                {alert.title}
              </h4>
              <p class="text-xs mt-1 text-base-content/80">{alert.message}</p>
            </div>
          {/each}
          <div class="divider my-1"></div>
        {/if}

        <!-- General Notifications Section -->
        {#if $notificationStore.isLoading}
          <div class="p-4 text-center">
            <span class="loading loading-spinner loading-md text-primary"></span>
          </div>
        {:else if $notificationStore.notifications.length === 0}
          <div class="p-6 text-center text-base-content/50">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 mx-auto mb-2 opacity-30" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" /></svg>
            <p>No notifications yet</p>
          </div>
        {:else}
          {#each $notificationStore.notifications as notification (notification.notification_id || notification.id)}
            <div 
              class="p-3 rounded-lg flex gap-3 transition-colors {!(notification.is_read || notification.read) ? 'bg-primary/5 hover:bg-primary/10' : 'hover:bg-base-200'}"
            >
              <div class="mt-1">
                {#if !(notification.is_read || notification.read)}
                  <div class="w-2 h-2 rounded-full bg-primary"></div>
                {/if}
              </div>
              <div class="flex-1 min-w-0">
                <h4 class="font-semibold text-sm truncate {notification.is_read || notification.read ? 'text-base-content/80' : ''}">
                  {notification.title || 'Notification'}
                </h4>
                <p class="text-xs mt-0.5 line-clamp-2 {notification.is_read || notification.read ? 'text-base-content/60' : ''}">
                  {notification.message}
                </p>
                {#if notification.created_at}
                  <p class="text-[10px] text-base-content/40 mt-1">
                    {new Date(notification.created_at).toLocaleDateString()}
                  </p>
                {/if}
              </div>
              {#if !(notification.is_read || notification.read)}
                <button 
                  class="btn btn-ghost btn-xs btn-circle text-primary" 
                  onclick={() => handleMarkAsRead(notification.notification_id || notification.id)}
                  title="Mark as read"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>
                </button>
              {/if}
            </div>
          {/each}
        {/if}
      </div>
      
      {#if $notificationStore.notifications.length > 0}
        <div class="p-2 border-t border-base-200 text-center bg-base-200/30">
          <button class="text-xs text-primary hover:underline font-medium">View all notifications</button>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>