'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),{spawn}=require('child_process'),{pathToFileURL,fileURLToPath}=require('url');
const ROOT=path.resolve(__dirname,'..'),SERVER=process.env.ABAPLINT_SERVER || '';
const CONFIG_SHA='c8c999cac95baa1ebec47b22d735dd9d743184c16073e84e303c78a6a1521146',SERVER_SHA='a5b462c564958592aafd41d2044ef2df2c22a4ad4df19b5d49577155a3b22587';
const hash=x=>crypto.createHash('sha256').update(x).digest('hex'),digest=p=>hash(fs.readFileSync(p));
const inside=(p,base)=>{const rel=path.relative(base,path.resolve(p));return rel===''||(!rel.startsWith('..')&&!path.isAbsolute(rel));};
const walk=d=>fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>{const p=path.join(d,e.name);if(e.isSymbolicLink())throw Error('SYMLINK_DENIED');return e.isDirectory()?walk(p):[p];});
async function validate(ws,targetNames,label,options={}){
 const started=Date.now(),out={label,utc:new Date().toISOString(),ws,targetNames,options,state:'VALIDATION_INVALID',reason:null,checks:{},files:{},transcript:[],stderr:''};
 let proc,closing=false,fatal=null,buffer=Buffer.alloc(0),id=0;const pending=new Map(),waiters=[],messages=[],readFiles=new Set();
 const record=(direction,message)=>out.transcript.push({ms:Date.now()-started,direction,message});
 const send=o=>{record('client',o);const b=Buffer.from(JSON.stringify(o));proc.stdin.write(`Content-Length: ${b.length}\r\n\r\n`);proc.stdin.write(b);};
 const signalError=e=>{fatal=e;for(const p of pending.values())p.reject(e);pending.clear();for(const w of waiters)w.reject(e);waiters.length=0;};
 const waitFor=(predicate,tag,ms=8000)=>new Promise((resolve,reject)=>{const found=messages.find(predicate);if(found)return resolve(found);if(fatal)return reject(fatal);const w={predicate,resolve:x=>{clearTimeout(w.timer);resolve(x);},reject:e=>{clearTimeout(w.timer);reject(e);}};w.timer=setTimeout(()=>{const ix=waiters.indexOf(w);if(ix>=0)waiters.splice(ix,1);reject(Error('TIMEOUT:'+tag));},ms);waiters.push(w);});
 const request=(method,params,ms=8000)=>new Promise((resolve,reject)=>{const reqid=++id;const timer=setTimeout(()=>{pending.delete(reqid);reject(Error('TIMEOUT:'+method));},ms);pending.set(reqid,{resolve:x=>{clearTimeout(timer);resolve(x);},reject:e=>{clearTimeout(timer);reject(e);}});send({jsonrpc:'2.0',id:reqid,method,params});});
 const notify=(method,params)=>send({jsonrpc:'2.0',method,params});
 let snapshot={};
 try{
  ws=path.resolve(ws);if(!inside(ws,ROOT)||!fs.existsSync(ws))throw Error('ROOT_INVALID');
  const configPath=path.join(ws,'abaplint.json');if(!fs.existsSync(configPath))throw Error('CONFIG_MISSING');
  const config=JSON.parse(fs.readFileSync(configPath,'utf8'));out.configSha256=digest(configPath);out.config=config;
  const approvedConfig=JSON.parse(fs.readFileSync(ROOT+'/config/approved.json'))[options.profile||'cloud'].sha256;
  if(out.configSha256!==approvedConfig)throw Error('CONFIG_FINGERPRINT_MISMATCH');
  if(config.dependencies.length)throw Error('DEPENDENCIES_DENIED');
  if(digest(SERVER)!==SERVER_SHA)throw Error('SERVER_IDENTITY_MISMATCH');
  out.checks.policy=true;
  const sources=walk(path.join(ws,'src'));snapshot=Object.fromEntries([configPath,...sources].map(p=>[p,digest(p)]));
  const sentinel=path.join(ws,'src','zcl_control.clas.abap');if(!fs.existsSync(sentinel))throw Error('CONTROL_MISSING');
  const frozen=JSON.parse(fs.readFileSync(ROOT+'/fixtures/frozen-contract.json'));
  if(digest(sentinel)!==frozen.controlSha256)throw Error('CONTROL_FINGERPRINT_MISMATCH');
  if(!targetNames.length)throw Error('TARGETS_EMPTY');
  for(const name of targetNames){if(!/\.(clas\.abap|intf\.abap|ddls\.asddls|bdef\.asbdef|tabl\.xml)$/.test(name))throw Error('TARGET_KIND_NOT_QUALIFIED');if(!inside(path.join(ws,'src',name),path.join(ws,'src'))||!sources.includes(path.join(ws,'src',name)))throw Error('TARGET_NOT_DISCOVERED');}
  const toPath=v=>{const p=path.resolve(/^file:/i.test(v)?fileURLToPath(v):v.replace(/^\/([a-z]:)/i,'$1')).replace(/^[a-z]:/,m=>m.toUpperCase());if(!inside(p,ws))throw Error('FS_OUTSIDE_WORKSPACE');if(fs.existsSync(p)&&!inside(fs.realpathSync(p),fs.realpathSync(ws)))throw Error('FS_LINK_ESCAPE');return p;};
  const serve=msg=>{
   const p=Array.isArray(msg.params)?msg.params[0]:msg.params;let result;
   try{
    if(options.stallFs&&msg.method!=='client/registerCapability')return;
    if(options.denyFs&&msg.method!=='client/registerCapability')throw Error('INJECTED_FS_DENIAL');
    switch(msg.method){
     case 'client/registerCapability':if(!msg.params.registrations.every(r=>r.method==='workspace/didChangeWorkspaceFolders'))throw Error('REGISTRATION_DENIED');result=null;break;
     case 'readFile': {const f=toPath(p);result=fs.readFileSync(f,'utf8');readFiles.add(f);break;}
     case 'exists':result=fs.existsSync(toPath(p));break;
     case 'isDirectory':result=fs.statSync(toPath(p)).isDirectory();break;
     case 'readdir':result=fs.readdirSync(toPath(p));break;
     case 'glob':if(p!=='/src/**/*.*')throw Error('GLOB_POLICY_MISMATCH:'+p);result=sources.map(f=>pathToFileURL(f).toString());out.checks.globDiscovered=result;break;
     default:throw Error('METHOD_DENIED:'+msg.method);
    }
    send({jsonrpc:'2.0',id:msg.id,result});
   }catch(e){send({jsonrpc:'2.0',id:msg.id,error:{code:-32000,message:e.message}});}
  };
  proc=spawn(options.startupFailure?path.join(ROOT,'missing-node.exe'):process.execPath,[SERVER,'--stdio'],{cwd:ws,stdio:['pipe','pipe','pipe'],windowsHide:true});
  proc.on('error',e=>signalError(Error('STARTUP:'+e.message)));
  proc.on('exit',(code,signal)=>{out.processExit={code,signal};if(!closing)signalError(Error('SERVER_EXIT:'+code+':'+signal));});
  proc.stdin.on('error',e=>{if(!closing)signalError(e);});
  proc.stderr.on('data',b=>out.stderr+=b.toString());
  proc.stdout.on('data',b=>{try{buffer=Buffer.concat([buffer,b]);for(;;){const end=buffer.indexOf('\r\n\r\n');if(end<0)return;const match=/Content-Length: (\d+)/i.exec(buffer.subarray(0,end).toString());if(!match)throw Error('PROTOCOL_HEADER');const len=+match[1];if(buffer.length<end+4+len)return;const msg=JSON.parse(buffer.subarray(end+4,end+4+len));buffer=buffer.subarray(end+4+len);record('server',msg);if(msg.method&&msg.id!==undefined){serve(msg);continue;}if(msg.id!==undefined){const p=pending.get(msg.id);if(p){pending.delete(msg.id);msg.error?p.reject(Error('PROTOCOL:'+JSON.stringify(msg.error))):p.resolve(msg.result);}continue;}messages.push(msg);for(let j=waiters.length-1;j>=0;j--)if(waiters[j].predicate(msg)){const w=waiters.splice(j,1)[0];w.resolve(msg);}}}catch(e){signalError(e);}});
  const rootUri=pathToFileURL(ws).toString();
  out.initialize=await request('initialize',{processId:process.pid,rootUri,workspaceFolders:[{uri:rootUri,name:'R2'}],capabilities:{workspace:{workspaceFolders:true,configuration:false},textDocument:{publishDiagnostics:{}}},initializationOptions:{provideFsProxy:!options.missingFsProxy,fallbackThreshold:2000}});
  out.checks.initialized=true;notify('initialized',{});
  // A real request triggers lazy Handler creation; ready status follows awaited load/parse.
  const controlUri=pathToFileURL(sentinel).toString();
  await request('textDocument/documentSymbol',{textDocument:{uri:controlUri}},options.stallFs?1200:8000);
  out.ready=(await waitFor(m=>m.method==='abaplint/status'&&m.params.text==='Ready','READY')).params;
  // Bundled Config maps legacy syntax.version=Cloud to Release.Newest=v816 + LanguageVersion.Cloud.
  const expectedVersion=JSON.parse(fs.readFileSync(ROOT+'/config/approved.json'))[options.profile||'cloud'].readyVersion;
  if(!out.ready.tooltip.includes('ABAP version: '+expectedVersion+'\n')||!out.ready.tooltip.includes('abaplint: 2.120.81')||!out.ready.tooltip.includes('Fallback activated: false'))throw Error('PROFILE_OR_FALLBACK_MISMATCH');
  if(!readFiles.has(configPath)||!messages.some(m=>m.method==='window/logMessage'&&m.params.message==='custom abaplint configuration found'))throw Error('CONFIG_NOT_LOADED');
  if(!messages.some(m=>m.method==='window/logMessage'&&m.params.message==='Workspace uri: '+rootUri))throw Error('WORKSPACE_NOT_REGISTERED');
  out.checks.configLoaded=true;out.checks.configurationReadHash=out.configSha256;
  const analyze=async(name,control=false)=>{
   const p=path.join(ws,'src',name),uri=pathToFileURL(p).toString();if(!readFiles.has(p))throw Error('SOURCE_NOT_LOADED:'+name);
   const start=out.transcript.length;let response;
   const publication=waitFor(m=>m.method==='textDocument/publishDiagnostics'&&m.params.uri===uri&&!(options.dropDiagnostic&&!control),'DIAGNOSTICS:'+name,options.dropDiagnostic?1200:8000);
   notify('textDocument/didOpen',{textDocument:{uri,languageId:'abap',version:1,text:fs.readFileSync(p,'utf8')}});
   response=await publication;
   if(!Array.isArray(response.params.diagnostics))throw Error('DIAGNOSTICS_INCOMPLETE');
   out.files[name]={hash:snapshot[p],diagnostics:response.params.diagnostics,lspTranscriptStart:start,lspTranscriptEnd:out.transcript.length};
   return response.params.diagnostics;
  };
  const controls=await analyze('zcl_control.clas.abap',true);
  if(options.missingControl||!controls.some(d=>d.code==='check_syntax'&&/lv_r2_missing/i.test(d.message)))throw Error('CONTROL_DIAGNOSTIC_MISSING');
  out.checks.control=true;
  if(options.crashAfterControl){proc.kill();await waitFor(()=>false,'CRASH',1200);}
  for(const name of targetNames)await analyze(name);
  if(options.mutateSource)fs.appendFileSync(path.join(ws,'src',targetNames[0]),'\n" injected unexpected change\n');
  if(options.mutateConfig)fs.appendFileSync(configPath,'\n');
  for(const [p,h]of Object.entries(snapshot))if(!fs.existsSync(p)||digest(p)!==h)throw Error('INPUT_CHANGED:'+path.basename(p));
  if(JSON.stringify(walk(path.join(ws,'src')).sort())!==JSON.stringify(sources.sort()))throw Error('SOURCE_INVENTORY_CHANGED');
  if(fatal)throw fatal;
  if(messages.some(m=>m.method==='window/logMessage'&&m.params.type===1))throw Error('SERVER_LOG_ERROR');
  out.checks.inputIntegrity=true;out.checks.completedPublications=targetNames.length;
  out.state=targetNames.some(n=>out.files[n].diagnostics.length)?'VALIDATION_FAIL':'VALIDATION_PASS';
 }catch(e){out.reason=e.message;out.state=/^STARTUP:/.test(e.message)?'VALIDATION_BLOCKED':'VALIDATION_INVALID';}
 finally{
  closing=true;
  if(proc&&proc.pid){try{await request('shutdown',null,1200);notify('exit',null);}catch(e){out.shutdownError=e.message;if(['VALIDATION_PASS','VALIDATION_FAIL'].includes(out.state)){out.state='VALIDATION_INVALID';out.reason='SHUTDOWN_INCOMPLETE';}}if(proc.exitCode===null&&proc.signalCode===null){const exited=new Promise(resolve=>{const t=setTimeout(resolve,1200);proc.once('close',()=>{clearTimeout(t);resolve();});});proc.kill();await exited;}}
  for(const p of pending.values())p.reject(Error('CLOSED'));for(const w of waiters)w.reject(Error('CLOSED'));
  out.elapsedMs=Date.now()-started;
  const dest=path.join(options.outputRoot,'logs',label+'.json');if(fs.existsSync(dest))throw Error('HISTORICAL_RUN_EXISTS:'+label);
  fs.writeFileSync(dest,JSON.stringify(out,null,2));
 }
 return out;
}
module.exports={validate,ROOT,SERVER,hash,digest};
