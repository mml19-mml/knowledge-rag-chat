const config = {
      darkMode: "class",
      theme: {
        extend: {
          colors: {
            "canvas-parchment": "#fbfbfd",
            "surface-pearl": "#f5f5f7",
            "ink": "#1d1d1f",
            "ink-muted-80": "#333333",
            "ink-muted-48": "#7a7a7a",
            "body-muted": "#86868b",
            "hairline": "#e5e5e7",
            "divider-soft": "rgba(0, 0, 0, 0.06)",
            "primary": "#004e9f",
            "primary-container": "#0066cc",
            "primary-focus": "#0071e3"
          },
          fontFamily: {
            sans: ["-apple-system", "BlinkMacSystemFont", "'SF Pro Display'", "'SF Pro Text'", "'Inter'", "sans-serif"],
            display: ["-apple-system", "BlinkMacSystemFont", "'SF Pro Display'", "'Inter'", "sans-serif"]
          },
          letterSpacing: {
            tighter: "-0.025em",
            tight: "-0.015em"
          }
        }
      }
    };
config.content=["./src/components/WelcomeDesign.vue"];
config.important=".design-welcome";
config.plugins=[require("@tailwindcss/forms"),require("@tailwindcss/container-queries")];
config.corePlugins={preflight:true};
module.exports=require("./theme-tokens.cjs")(config);
