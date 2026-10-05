// Apply the saved theme before the page paints. Only this preference is persisted.
(function () {
  var theme = 'light';
  try {
    if (localStorage.getItem('knowledge-chat-theme') === 'dark') theme = 'dark';
  } catch (_) {
    // Storage can be unavailable in a restricted browser session.
  }
  document.documentElement.dataset.theme = theme;
  document.documentElement.style.colorScheme = theme;
  document.documentElement.style.backgroundColor = theme === 'dark' ? '#090909' : '#fbfbfd';
})();
