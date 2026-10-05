import { computed, ref } from 'vue';

type Theme = 'light' | 'dark';
const storageKey = 'knowledge-chat-theme';
const current = ref<Theme>(document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light');

function applyTheme(value: Theme) {
  current.value = value;
  document.documentElement.dataset.theme = value;
  document.documentElement.style.colorScheme = value;
  document.documentElement.style.backgroundColor = value === 'dark' ? '#090909' : '#fbfbfd';
}

function toggleTheme() {
  applyTheme(current.value === 'dark' ? 'light' : 'dark');
  try {
    localStorage.setItem(storageKey, current.value);
  } catch {
    // The switch still works for this page when persistence is unavailable.
  }
}

// Keep chat and admin tabs consistent without storing any conversation or key.
window.addEventListener('storage', (event) => {
  if (event.key === storageKey || event.key === null) {
    applyTheme(event.newValue === 'dark' ? 'dark' : 'light');
  }
});

export function useTheme() {
  return { isDark: computed(() => current.value === 'dark'), toggleTheme };
}
