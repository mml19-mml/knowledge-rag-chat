<script setup lang="ts">
import ThemeSwitch from "./ThemeSwitch.vue";
const question=defineModel<string>({required:true});
defineProps<{busy:boolean;error:string}>();const emit=defineEmits<{send:[]}>();
function keyboard(e:KeyboardEvent){if(e.key==='Enter'&&!e.shiftKey&&!e.isComposing){e.preventDefault();emit('send')}}
function resize(e:Event){const el=e.target as HTMLTextAreaElement;el.style.height='auto';el.style.height=Math.min(el.scrollHeight,240)+'px'}
</script>
<template><div class="design-welcome"><div class="design-body min-h-screen bg-canvas bg-atlas text-ink flex flex-col justify-between selection:bg-blue-100 selection:text-primary-container antialiased">

<header class="w-full max-w-6xl mx-auto px-6 py-6 sm:px-10 flex justify-between items-center z-10" data-purpose="top-navigation">

<div class="flex items-center gap-2.5">
<div class="w-7 h-7 rounded-lg ui-logo flex items-center justify-center shadow-sm">
<svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" viewBox="0 0 24 24">
<path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
</svg>
</div>
<span class="text-[17px] sm:text-lg font-semibold tracking-tight text-ink font-display">
        Knowledge Chat
      </span>
<span class="ui-curated-badge inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-medium tracking-wide bg-surface-secondary text-body-muted border border-hairline/60">
        CURATED BASE
      </span>
</div>

<div class="header-actions">
<ThemeSwitch />
<button class="press-action px-3.5 py-1.5 rounded-full text-xs font-medium text-body-muted hover:text-ink bg-surface/80 hover:bg-surface border border-hairline shadow-[0_1px_2px_rgba(0,0,0,0.03)] flex items-center gap-1.5" data-purpose="clear-conversation-trigger" id="clear-chat-btn" aria-label="Clear input" title="Clear input" @click="question=''" type="button">
<svg class="w-3.5 h-3.5 text-ink-muted-48" fill="none" stroke="currentColor" stroke-width="1.8" viewBox="0 0 24 24">
<path d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" stroke-linecap="round" stroke-linejoin="round"></path>
</svg>
<span>Clear Chat</span>
</button>
</div>
</header>


<main class="flex-1 flex flex-col items-center justify-center px-4 sm:px-6 w-full -mt-4 pb-12">
<div class="w-full max-w-2xl flex flex-col items-center text-center">

<div class="mb-5 inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full text-[12px] font-medium text-emerald-800 bg-emerald-50/90 border border-emerald-200/50 shadow-sm" data-purpose="knowledge-source-badge">
<span class="relative flex h-2 w-2">
<span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
<span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
</span>
<span class="tracking-tight">Based on Curated Knowledge</span>
</div>

<h1 class="text-4xl sm:text-5xl lg:text-[52px] font-semibold text-ink tracking-tighter leading-[1.08] mb-3.5 font-display">
        What would you like to know?
      </h1>

<p class="text-[15px] sm:text-base text-body-muted font-normal leading-relaxed max-w-lg">
        Searching across indexed documentation with verified citations.
      </p>

<p class="text-xs text-ink-muted-48 mt-1 mb-8 font-normal">
        Please provide a specific query. Sources will be cited when available.
      </p><div class="ui-hero-robot relative flex justify-center items-end -mb-8 z-0 pointer-events-none select-none"><img alt="Knowledge AI Assistant" class="w-56 sm:w-64 md:w-72 h-auto max-h-72 object-contain drop-shadow-[0_12px_24px_rgba(0,102,204,0.08)] filter" src="/robot-welcome.png"/></div>

<div class="w-full apple-card p-6 text-left relative z-10" data-purpose="query-composer-card">

<label class="block text-[11px] font-semibold text-ink-muted-48 uppercase tracking-wider mb-2.5" for="question-textarea">
          Your Question
        </label>

<textarea class="w-full resize-none border-0 p-0 text-ink text-base placeholder:text-body-muted/70 focus:ring-0 bg-transparent leading-relaxed focus:outline-none" id="question-textarea" v-model="question" maxlength="1000" :disabled="busy" @keydown="keyboard" @input="resize" placeholder="Ask anything about the knowledge base..." rows="3"></textarea>

<div class="mt-4 pt-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-t border-divider-soft">
<p class="text-[12px] text-body-muted tracking-tight select-none">
            Answers are grounded strictly in your uploaded knowledge.
          </p>
<button class="ui-primary-action press-action self-end sm:self-auto inline-flex items-center justify-center gap-1.5 px-5 py-2.5 rounded-full text-[13px] font-medium text-on-action bg-action hover:bg-action-hover shadow-[0_1px_2px_rgba(0,102,204,0.2)] hover:shadow-md transition-all" data-purpose="submit-query" id="send-button" @click="$emit('send')" :disabled="busy || !question.trim()" type="button">
<span>{{busy?'Searching…':'Ask Knowledge'}}</span>
<svg class="w-3.5 h-3.5 stroke-[2.5]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
<path d="M4.5 19.5l15-15m0 0H8.25m11.25 0v11.25" stroke-linecap="round" stroke-linejoin="round"></path>
</svg>
</button>
</div>
</div>
<p v-if="error" role="alert" class="text-red-700 text-sm mt-4">{{error}}</p>
</div>
</main>


<footer class="w-full py-6 text-center text-xs text-body-muted font-normal">
    Powered by Knowledge Base Engine
  </footer>



</div></div></template>
<style scoped>

    .design-body {
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Inter", "Segoe UI", Roboto, sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }

    /* Ambient Atlas canvas backdrop */
    .bg-atlas {
      background: var(--ui-welcome-backdrop);
    }

    /* Apple-grade elevated floating prompt card */
    .apple-card {
      background: rgb(var(--ui-surface));
      border-radius: 24px;
      border: 1px solid rgb(var(--ui-hairline));
      box-shadow: var(--ui-card-shadow);
      transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .apple-card:hover,
    .apple-card:focus-within {
      transform: translateY(-2px);
      box-shadow: 0 16px 36px -6px rgba(0, 0, 0, 0.06), 0 1px 3px rgba(0, 0, 0, 0.03);
      border-color: rgb(var(--ui-link) / .4);
    }

    /* Spring micro-interaction */
    .press-action {
      transition: transform 0.15s cubic-bezier(0.34, 1.56, 0.64, 1), background-color 0.2s ease, box-shadow 0.2s ease;
    }

    .press-action:active {
      transform: scale(0.96) !important;
    }

    /* Subtle custom scrollbar */
    textarea::-webkit-scrollbar {
      width: 4px;
    }
    textarea::-webkit-scrollbar-thumb {
      background: rgb(var(--ui-hairline));
      border-radius: 9999px;
    }
    textarea::-webkit-scrollbar-thumb:hover {
      background: rgb(var(--ui-muted));
    }
  
.design-body{min-height:100vh}button:disabled{cursor:not-allowed;opacity:.55}button:focus-visible,a:focus-visible{outline:2px solid rgb(var(--ui-link));outline-offset:3px}
</style>
