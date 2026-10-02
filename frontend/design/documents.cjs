const config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            "primary": "#0066cc",
            "primary-focus": "#0071e3",
            "primary-hover": "#0052a3",
            "ink": "#1d1d1f",
            "ink-muted-80": "#333333",
            "ink-muted-48": "#7a7a7a",
            "body-muted": "#86868b",
            "hairline": "#e5e5e7",
            "surface-card": "#ffffff",
            "surface-pearl": "#f5f5f7",
            "canvas-parchment": "#fbfbfd",
            "outline-subtle": "rgba(0, 0, 0, 0.08)"
          },
          boxShadow: {
            'apple-card': '0 4px 24px -2px rgba(16, 42, 67, 0.04), 0 1px 3px 0 rgba(0, 0, 0, 0.02)',
            'apple-elevated': '0 16px 40px -8px rgba(0, 0, 0, 0.07), 0 2px 6px 0 rgba(0, 0, 0, 0.03)',
            'subtle-inner': 'inset 0 1px 2px rgba(0, 0, 0, 0.03)'
          },
          fontFamily: {
            body: ["-apple-system", "BlinkMacSystemFont", "'SF Pro Text'", "'Inter'", "sans-serif"],
            display: ["-apple-system", "BlinkMacSystemFont", "'SF Pro Display'", "'Inter'", "sans-serif"]
          }
        }
      }
    };
config.content=["./src/components/DocumentsDesign.vue"];
config.important=".design-documents";
config.plugins=[require("@tailwindcss/forms"),require("@tailwindcss/container-queries")];
config.corePlugins={preflight:false};
module.exports=config;
