export const $ = s=>document.querySelector(s);
export const esc = v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
export const icon = name=>`<span class="icon" aria-hidden="true">${name}</span>`;
export function toast(message){$('#toast').textContent=message;$('#toast').hidden=false;clearTimeout(toast.timer);toast.timer=setTimeout(()=>$('#toast').hidden=true,2600)}
export function getStored(key,fallback){try{return JSON.parse(localStorage.getItem(key))??fallback}catch{return fallback}}
export function saveStored(key,value){try{localStorage.setItem(key,JSON.stringify(value));return true}catch{return false}}
export function setTheme(value){window.KnowledgeNative?.setTheme(value);document.documentElement.dataset.theme=value;document.body.dataset.theme=value;saveStored('split-demo-theme',value);document.querySelectorAll('[data-action="theme"]').forEach(b=>{b.setAttribute('aria-checked',String(value==='dark'));b.setAttribute('title',value==='dark'?'切换浅色':'切换夜间')});document.querySelectorAll('[data-theme-choice]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.themeChoice===value)));}
export function toggleTheme(){setTheme(document.documentElement.dataset.theme==='dark'?'light':'dark')}
export function themeSwitch(){return `<button class="theme-toggle" data-action="theme" role="switch" aria-label="夜间模式" aria-checked="${document.documentElement.dataset.theme==='dark'}"><span class="theme-thumb"></span>${icon('light_mode')}${icon('dark_mode')}</button>`}
export function dialog(title,body,actions=''){$('#dialog-title').textContent=title;$('#dialog-body').innerHTML=body;$('#dialog-actions').innerHTML=actions;$('#dialog').showModal()}
export async function copy(text){try{if(window.KnowledgeNative)window.KnowledgeNative.copyText(text);else await navigator.clipboard.writeText(text);toast('已复制回答')}catch{toast('复制未完成，请选择文字后复制')}}
export function download(name,content){if(window.KnowledgeNative){window.KnowledgeNative.exportJson(name,content);return}const url=URL.createObjectURL(new Blob([content],{type:'application/json;charset=utf-8'}));const a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000)}
document.addEventListener('click',e=>{if(e.target.closest('[data-close]'))$('#dialog').close();if(e.target.closest('[data-action="theme"]'))toggleTheme();const choice=e.target.closest('[data-theme-choice]');if(choice)setTheme(choice.dataset.themeChoice)});
$('#dialog').addEventListener('click',e=>{if(e.target!==$('#dialog'))return;const r=e.target.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)e.target.close()});
setTheme(getStored('split-demo-theme','light')==='dark'?'dark':'light');
