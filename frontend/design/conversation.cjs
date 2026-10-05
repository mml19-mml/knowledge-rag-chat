const config = {
      theme: {
        extend: {
          colors: {
            primary: '#0066cc',
            'primary-hover': '#0071e3',
            'primary-focus': '#0071e3',
            'primary-dark': '#004e9f',
            ink: '#1d1d1f',
            'ink-muted': '#86868b',
            'ink-subtle': '#6e6e73',
            hairline: '#e5e5e7',
            canvas: '#fbfbfd',
            surface: '#ffffff',
            'surface-secondary': '#f5f5f7',
            'badge-agent': '#f0f2f5'
          },
          fontFamily: {
            sans: ['-apple-system', 'BlinkMacSystemFont', '"SF Pro Text"', '"SF Pro Display"', 'Inter', 'sans-serif']
          },
          boxShadow: {
            'apple-card': '0 4px 20px 0 rgba(0, 0, 0, 0.03), 0 1px 2px 0 rgba(0, 0, 0, 0.04)',
            'apple-floating': '0 12px 32px -4px rgba(0, 0, 0, 0.06), 0 1px 2px 0 rgba(0, 0, 0, 0.04)',
            'button-tap': '0 1px 2px rgba(0, 0, 0, 0.12)'
          }
        }
      }
    };
config.content=["./src/components/ConversationDesign.vue"];
config.important=".design-conversation";
config.plugins=[require("@tailwindcss/forms"),require("@tailwindcss/container-queries")];
config.corePlugins={preflight:false};
module.exports=require("./theme-tokens.cjs")(config);
