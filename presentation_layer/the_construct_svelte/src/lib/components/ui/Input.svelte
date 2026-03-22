<script lang="ts">
  import type { EventHandler } from 'svelte/elements';

  let {
    type = 'text',
    value = $bindable(''),
    placeholder = '',
    label = '',
    error = '',
    disabled = false,
    required = false,
    readonly = false,
    size = 'md',
    fullWidth = false,
    id = '',
    name = '',
    autocomplete = '',
    min = undefined,
    max = undefined,
    step = undefined,
    minlength = undefined,
    maxlength = undefined,
    onchange,
    oninput,
    onfocus,
    onblur
  }: {
    type?: 'text' | 'email' | 'password' | 'number' | 'tel' | 'url' | 'search';
    value?: string | number | undefined;
    placeholder?: string;
    label?: string;
    error?: string;
    disabled?: boolean;
    required?: boolean;
    readonly?: boolean;
    size?: 'sm' | 'md' | 'lg';
    fullWidth?: boolean;
    id?: string;
    name?: string;
    autocomplete?: string;
    min?: number | undefined;
    max?: number | undefined;
    step?: number | undefined;
    minlength?: number | undefined;
    maxlength?: number | undefined;
    onchange?: EventHandler<Event, HTMLInputElement>;
    oninput?: EventHandler<Event, HTMLInputElement>;
    onfocus?: EventHandler<FocusEvent, HTMLInputElement>;
    onblur?: EventHandler<FocusEvent, HTMLInputElement>;
  } = $props();

  let inputClasses = $derived([
    'input',
    `input-${size}`,
    error && 'input-error',
    disabled && 'input-disabled',
    fullWidth && 'w-full',
    'transition-all duration-200 ease-in-out'
  ].filter(Boolean).join(' '));

  let inputId = $derived(id || `input-${Math.random().toString(36).substr(2, 9)}`);
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
    {minlength}
    {maxlength}
    id={inputId}
    class={inputClasses}
    bind:value
    {onchange}
    {oninput}
    {onfocus}
    {onblur}
  />
  
  {#if error}
    <label class="label" for={inputId}>
      <span class="label-text-alt text-error">{error}</span>
    </label>
  {/if}
</div>

<style>
  /* svelte-ignore css_unknown_at_rule */
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