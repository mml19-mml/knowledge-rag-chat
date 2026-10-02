const config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            "primary": "#004e9f",
            "primary-container": "#0066cc",
            "primary-focus": "#0071e3",
            "ink": "#1d1d1f",
            "ink-muted-80": "#333333",
            "ink-muted-48": "#7a7a7a",
            "body-muted": "#86868b",
            "surface-card": "#ffffff",
            "surface-pearl": "#f5f5f7",
            "canvas-parchment": "#fbfbfd",
            "divider-soft": "rgba(0, 0, 0, 0.06)",
            "hairline": "#e5e5e7",
          },
          fontFamily: {
            sans: [
              "-apple-system",
              "BlinkMacSystemFont",
              "'SF Pro Display'",
              "'SF Pro Text'",
              "'Inter'",
              "sans-serif"
            ],
          },
          boxShadow: {
            'apple-whisper': '0 4px 20px -2px rgba(0, 0, 0, 0.04), 0 2px 6px -1px rgba(0, 0, 0, 0.02)',
            'apple-float': '0 20px 40px -15px rgba(0, 0, 0, 0.06), 0 0 1px 1px rgba(0, 0, 0, 0.04)',
            'apple-input': 'inset 0 1px 2px rgba(0, 0, 0, 0.03)',
            'apple-focus': '0 0 0 4px rgba(0, 113, 227, 0.16)'
          }
        }
      }
    };
config.content=["./src/components/AuthDesign.vue"];
config.important=".design-auth";
config.plugins=[require("@tailwindcss/forms"),require("@tailwindcss/container-queries")];
config.corePlugins={preflight:false};
module.exports=config;
