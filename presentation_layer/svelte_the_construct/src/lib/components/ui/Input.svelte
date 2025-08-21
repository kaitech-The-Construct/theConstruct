<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let type: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search' = 'text';
  export let value: string | number = '';
  export let placeholder: string = '';
  export let label: string = '';
  export let error: string = '';
  export let disabled: boolean = false;
  export let required: boolean = false;
  export let readonly: boolean = false;
  export let size: 'sm' | 'md' | 'lg' = 'md';
  export let fullWidth: boolean = false;
  export let id: string = '';
  export let name: string = '';
  export let autocomplete: string = '';
  export let min: number | undefined = undefined;
  export let max: number | undefined = undefined;
  export let step: number | undefined = undefined;

  const dispatch = createEventDispatcher();

  function handleInput(event: Event) {
    const target = event.target as HTMLInputElement;
    value = type === 'number' ? Number(target.value) : target.value;
    dispatch('input', { value, event });
  }

  function handleChange(event: Event) {
    dispatch('change', { value, event });
  }

  function handleFocus(event: FocusEvent) {
    dispatch('focus', event);
  }

  function handleBlur(event: FocusEvent) {
    dispatch('blur', event);
  }

  $: inputClasses = [
    'input',
    `input-${size}`,
    error && 'input-error',
    disabled && 'input-disabled',
    fullWidth && 'w-full',
    'transition-all duration-200 ease-in-out'
  ].filter(Boolean).join(' ');

  $: inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`;
</script>

<div class="form-control" class:w-full={fullWidth}>
  {#if label}
    <label class="label" for={inputId}>
      <span class="label-text">
        {label}
        {#if required}
          <span class="text-error">*</span>
        {/if}
      </span>
    </label>
  {/if}
  
  <input
    {type}
    {placeholder}
    {disabled}
    {required}
    {readonly}
    {name}
    {autocomplete}
    {min}
    {max}
    {step}
    id={inputId}
    class={inputClasses}
    bind:value
    on:input={handleInput}
    on:change={handleChange}
    on:focus={handleFocus}
    on:blur={handleBlur}
  />
  
  {#if error}
    <label class="label" for={inputId}>
      <span class="label-text-alt text-error">{error}</span>
    </label>
  {/if}
</div>

<style>
  .input {
    @apply w-full px-3 py-2 border border-base-300 rounded-md 
           bg-base-100 text-base-content
           focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent
           disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-base-200
           placeholder:text-base-content/50;
  }

  .input-sm {
    @apply px-2 py-1 text-sm;
  }

  .input-md {
    @apply px-3 py-2 text-base;
  }

  .input-lg {
    @apply px-4 py-3 text-lg;
  }

  .input-error {
    @apply border-error focus:ring-error;
  }

  .input-disabled {
    @apply opacity-50 cursor-not-allowed bg-base-200;
  }

  .form-control {
    @apply flex flex-col gap-1;
  }

  .label {
    @apply flex justify-between items-center;
  }

  .label-text {
    @apply text-sm font-medium text-base-content;
  }

  .label-text-alt {
    @apply text-xs;
  }
</style>
