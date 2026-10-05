<script setup lang="ts">
import { useTheme } from '../theme';
const { isDark, toggleTheme } = useTheme();
</script>

<template>
  <button
    class="theme-switch"
    type="button"
    role="switch"
    aria-label="夜间模式"
    :aria-checked="isDark"
    :title="isDark ? '切换到浅色模式' : '切换到夜间模式'"
    @click="toggleTheme"
  >
    <span class="theme-switch-track" aria-hidden="true">
      <span class="theme-switch-thumb"></span>
      <svg class="theme-switch-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round">
        <circle cx="12" cy="12" r="3.5" />
        <path d="M12 2v2m0 16v2M2 12h2m16 0h2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
      </svg>
      <svg class="theme-switch-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
        <path d="M20.9 13.3A9 9 0 0 1 10.7 3.1 9 9 0 1 0 20.9 13.3Z" />
      </svg>
    </span>
  </button>
</template>

<style scoped>
.theme-switch {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: 0 0 60px;
  width: 60px;
  height: 44px;
  padding: 0;
  border: 0;
  background: transparent;
  cursor: pointer;
  border-radius: 999px;
}
.theme-switch-track {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-around;
  width: 58px;
  height: 30px;
  border: 1px solid rgb(var(--ui-hairline));
  border-radius: 999px;
  background: rgb(var(--ui-secondary));
  color: rgb(var(--ui-muted));
}
.theme-switch-thumb {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 22px;
  height: 22px;
  border-radius: 50%;
  background: rgb(var(--ui-surface));
  box-shadow: 0 1px 4px #0002;
  transition: transform 180ms ease, background-color 180ms ease;
}
svg { z-index: 1; width: 15px; height: 15px; }
.theme-switch-sun { color: rgb(var(--ui-ink)); }
[aria-checked='true'] .theme-switch-thumb { transform: translateX(28px); background: #fff; }
[aria-checked='true'] .theme-switch-sun { color: rgb(var(--ui-muted)); }
[aria-checked='true'] .theme-switch-moon { color: #171717; }
.theme-switch:hover .theme-switch-track { border-color: rgb(var(--ui-muted)); }
.theme-switch:focus-visible { outline: 2px solid rgb(var(--ui-link)); outline-offset: 3px; }
</style>
