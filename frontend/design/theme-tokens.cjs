// Shared semantic palette for all four exported Stitch screens. RGB channels
// retain Tailwind opacity modifiers without duplicating light/dark templates.
const color = (token) => `rgb(var(--ui-${token}) / <alpha-value>)`;
module.exports = (config) => {
  Object.assign(config.theme.extend.colors, {
    canvas: color('canvas'), 'canvas-parchment': color('canvas'),
    surface: color('surface'), 'surface-card': color('surface'),
    'surface-secondary': color('secondary'), 'surface-pearl': color('secondary'),
    'badge-agent': color('secondary'), ink: color('ink'),
    'ink-muted-80': color('body'), 'ink-muted-48': color('muted'),
    'ink-muted': color('muted'), 'ink-subtle': color('muted'), 'body-muted': color('muted'),
    hairline: color('hairline'), 'divider-soft': color('hairline'),
    'outline-subtle': color('hairline'), primary: color('link'),
    'primary-container': color('link'), 'primary-hover': color('link'),
    'primary-focus': color('link'), 'primary-dark': color('link'),
    'on-action': color('on-action'), action: color('action'), 'action-hover': color('action-hover'),
    'success-tint': color('success-tint'), success: color('success'),
    'link-tint': color('link-tint'), danger: color('danger'),
    // Utility aliases retained by the original exported markup.
    slate: {
      50: color('secondary'), 100: color('secondary'), 200: color('hairline'),
      300: color('hairline'), 400: color('muted'), 600: color('body'),
      700: color('body'), 800: color('body'), 900: color('mascot'),
    },
    blue: { 50: color('link-tint'), 100: color('link-border'), 400: color('link'), 500: color('link'), 600: color('link'), 900: color('link') },
    emerald: { 50: color('success-tint'), 200: color('success-border'), 400: '#34d399', 500: '#22c55e', 700: color('success'), 800: color('success') },
    red: { 500: color('danger'), 700: color('danger') },
  });
  config.theme.extend.boxShadow = {
    ...config.theme.extend.boxShadow,
    'apple-card': 'var(--ui-card-shadow)',
    'apple-float': 'var(--ui-card-shadow)',
    'apple-elevated': 'var(--ui-card-shadow)',
  };
  return config;
};
