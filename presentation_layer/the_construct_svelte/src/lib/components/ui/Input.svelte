<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let type: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search' = 'text';
  export let value: string | number | undefined = '';
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

  let inputValue: string | number | undefined = value;

  $: if (value !== inputValue) {
    inputValue = value;
  }

  function handleInput(event: Event) {
    const target = event.target as HTMLInputElement;
    if (type === 'number') {
      inputValue = target.valueAsNumber;
      value = target.valueAsNumber;
    } else {
      inputValue = target.value;
      value = target.value;
    }
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
    autocomplete={autocomplete as any}
    {min}
    {max}
    {step}
    id={inputId}
    class={inputClasses}
    bind:value={inputValue}
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
  @reference "../../../app.css";
  .input {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 1px solid var(--base-300);
    border-radius: 0.375rem;
    background-color: var(--base-100);
    color: var(--base-content);
    transition: all 0.2s ease-in-out;
  }

  .input:focus {
    outline: none;
    box-shadow: 0 0 0 2px var(--primary);
    border-color: transparent;
  }

  .input:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    background-color: var(--base-200);
  }

  .input::placeholder {
    color: rgba(var(--base-content), 0.5);
  }

  .input-sm {
    padding: 0.25rem 0.5rem;
    font-size: 0.875rem;
  }

  .input-md {
    padding: 0.5rem 0.75rem;
    font-size: 1rem;
  }

  .input-lg {
    padding: 0.75rem 1rem;
    font-size: 1.125rem;
  }

  .input-error {
    border-color: var(--error);
  }

  .input-error:focus {
    box-shadow: 0 0 0 2px var(--error);
  }

  .input-disabled {
    opacity: 0.5;
    cursor: not-allowed;
    background-color: var(--base-200);
  }

  .form-control {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .label {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .label-text {
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--base-content);
  }

  .label-text-alt {
    font-size: 0.75rem;
  }
</style>
