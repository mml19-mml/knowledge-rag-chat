import {getStored,saveStored} from './ui.js';

const KEY='knowledge-apk-connection';
let config=getStored(KEY,{mode:'offline',baseUrl:''});
if(!config || !['offline','rag'].includes(config.mode))config={mode:'offline',baseUrl:''};
export const connection=()=>({...config});
export const modeLabel=()=>config.mode==='rag'?'RAG 服务':'离线演示';
export function normalizeAddress(value){
  let parsed;
  try{parsed=new URL(value.trim())}catch{throw new Error('请输入完整地址，例如 http://192.168.1.10:8000')}
  if(!['http:','https:'].includes(parsed.protocol)||parsed.username||parsed.password||parsed.search||parsed.hash)throw new Error('服务地址需以 http:// 或 https:// 开头，不能包含账号或查询参数。');
  if(['localhost','127.0.0.1','[::1]'].includes(parsed.hostname))throw new Error('手机上的 localhost 指手机本身，请填写电脑的局域网 IP 或线上地址。');
  return parsed.toString().replace(/\/+$/,'');
}
export function saveConnection(mode,baseUrl){
  if(!['offline','rag'].includes(mode))throw new Error('请选择问答模式。');
  const address=mode==='rag'?normalizeAddress(baseUrl):(baseUrl||'').trim();
  if(!saveStored(KEY,{mode,baseUrl:address}))throw new Error('设置未能保存，请重试。');
  config={mode,baseUrl:address};
}
const pending=new Map();
window.__nativeReply=(id,response)=>{const entry=pending.get(id);if(entry){clearTimeout(entry.timer);pending.delete(id);entry.resolve(response)}};
async function request(base,operation,payload={}){
  let result;
  if(window.KnowledgeNative){
    result=await new Promise((resolve,reject)=>{
      const id=crypto.randomUUID();
      const timer=setTimeout(()=>{pending.delete(id);reject(new Error('服务响应超时，请检查后端状态后重试。'))},operation==='ask'?135000:15000);
      pending.set(id,{resolve,timer});
      try{window.KnowledgeNative.request(id,base,operation,JSON.stringify(payload))}catch{clearTimeout(timer);pending.delete(id);reject(new Error('无法发起请求，请重新打开应用。'))}
    });
  }else{
    const controller=new AbortController();const timer=setTimeout(()=>controller.abort(),operation==='ask'?130000:14000);
    try{const response=await fetch(base+(operation==='ask'?'/api/rag/ask':operation==='health'?'/api/health':'/health'),{method:operation==='ask'?'POST':'GET',headers:operation==='ask'?{'Content-Type':'application/json'}:{},body:operation==='ask'?JSON.stringify(payload):undefined,signal:controller.signal});result={ok:response.ok,status:response.status,body:await response.text()}}
    catch{throw new Error('连接失败，请检查服务地址、网络及电脑上的 RAG 服务。')}
    finally{clearTimeout(timer)}
  }
  if(!result.ok){const error=new Error(result.error||`服务返回 HTTP ${result.status}，请检查服务配置。`);error.status=result.status;throw error;}
  try{return JSON.parse(result.body)}catch{throw new Error('该地址没有返回有效的 RAG 接口数据。')}
}
export async function checkConnection(base){
  const address=normalizeAddress(base);
  let result;
  try{result=await request(address,'health')}
  catch(error){if(error.status!==404)throw error;result=await request(address,'health-legacy')}
  if(result.status!=='ok')throw new Error('服务未返回正常的健康状态。');
  return result;
}
export async function ask(question){
  if(question.length>1000)throw new Error('问题请控制在 1000 字以内。');
  if(config.mode==='offline'){
    await new Promise(resolve=>setTimeout(resolve,650));
    const method=/方法|流程|判断|取舍/.test(question);
    return {answer:method?'这是一段离线演示回答，用来测试手机上的问答交互。\n\n可以用一个真实案例展示工作方法：\n1. 明确问题和成功标准。\n2. 比较可选方案，记录取舍依据。\n3. 小范围验证，观察结果。\n4. 复盘后再迭代。\n\n这里没有读取你的个人资料，也没有调用大模型。在 Setting 中连接 RAG 服务后，才能获得资料问答。':'这是一段离线演示回答，用来测试手机上的问答交互。\n\n介绍项目经历时，可以按以下顺序组织：\n1. 背景：要解决谁的什么问题。\n2. 职责：你实际负责的部分。\n3. 行动：关键选择和推进过程。\n4. 结果：可核实的成果与复盘。\n\n这里没有读取你的个人资料，也没有调用大模型。在 Setting 中连接 RAG 服务后，才能获得资料问答。',mode:'offline',sources:[{id:method?'sample-method':'sample-project',filename:method?'示例-工作方法.pdf':'示例-项目经历.pdf',page:1,sample:true,excerpt:method?'示例摘录：明确问题、比较方案、验证假设、复盘迭代。':'示例摘录：项目背景、个人职责、关键行动、结果和复盘。'}]};
  }
  const result=await request(normalizeAddress(config.baseUrl),'ask',{question,limit:5,document_id:null});
  if(typeof result.answer!=='string'||!result.answer.trim())throw new Error('服务没有返回回答，请检查知识库与模型配置。');
  const requestId=crypto.randomUUID();
  return {answer:result.answer,mode:result.is_placeholder?'placeholder':'rag',sources:(Array.isArray(result.sources)?result.sources:[]).map((source,index)=>({id:`${requestId}-${index}`,filename:source.filename||'知识库资料',page:source.page_start||null,sample:false,excerpt:'此接口返回了引用文件和页码，未提供每条引用对应的原文片段。请在资料管理端核对原文。'}))};
}
