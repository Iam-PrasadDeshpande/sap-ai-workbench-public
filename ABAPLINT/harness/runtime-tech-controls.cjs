'use strict';
const fs=require('fs'),path=require('path'),vm=require('vm');
const R=path.resolve(__dirname,'..'),P=path.resolve(R,'node_modules/@abaplint');
const {Transpiler}=require(P+'/transpiler'),{ABAP,MemoryConsole}=require(P+'/runtime');
const cases=JSON.parse(fs.readFileSync(R+'/supplements/technical_revalidation/controls.json'));
async function run(id,label=id){const c=cases.find(c=>c.id===id);if(!c)throw Error('Unknown case');const out=path.join(process.env.ABAPLINT_OUTPUT_ROOT,'runtime',label);fs.mkdirSync(out,{recursive:true});const r={id,label,utc:new Date().toISOString(),stages:{},checks:[],sqlTrace:[],sap:'SAP_EVIDENCE_REQUIRED',engine:'@abaplint/transpiler/runtime 2.14.8',phase:'transpile'};let db;
try{
 const output=await new Transpiler({addCommonJS:false}).runRaw(Object.entries(c.files).map(([filename,contents])=>({filename,contents})));r.stages.transpiled=true;
 fs.writeFileSync(out+'/database-setup.json',JSON.stringify(output.databaseSetup,null,2));
 const abap=new ABAP({console:new MemoryConsole()});globalThis.abap=abap;abap.builtin.sy.get().mandt.set('100');
 if(c.sql){const {DatabaseSync}=require('node:sqlite');db=new DatabaseSync(':memory:');r.database='Node built-in SQLite, in-memory, custom minimal adapter; not SAP HANA';
 db.exec('CREATE TABLE zr4_data ('+(c.sql.client?'mandt TEXT, ':'')+'id INTEGER, amount INTEGER'+(c.sql.notNull?' NOT NULL DEFAULT 0':'')+')');
 const stmt=db.prepare('INSERT INTO zr4_data VALUES ('+(c.sql.client?'?,?,?':'?,?')+')');for(const row of c.sql.rows)stmt.run(...row);
 let active=false;const begin=async()=>{if(!active){db.exec('BEGIN');active=true;}};
 abap.context.databaseConnections.DEFAULT={name:'sqlite',beginTransaction:begin,commit:async()=>{r.sqlTrace.push({operation:'commit',active});if(active){db.exec('COMMIT');active=false;}},rollback:async()=>{r.sqlTrace.push({operation:'rollback',active});if(active){db.exec('ROLLBACK');active=false;}},select:async o=>{r.sqlTrace.push({operation:'select',sql:o.select});const sql=o.select.replace(/ UP TO (\d+) ROWS\s*$/i,' LIMIT $1'); r.sqlTrace.push({operation:'dialect_translation',original:o.select,sqlite:sql}); return {rows:db.prepare(sql).all()};},insert:async o=>{await begin();const sql=`INSERT INTO ${o.table} (${o.columns.join(',')}) VALUES (${o.values.join(',')})`;r.sqlTrace.push({operation:'insert',sql});const x=db.prepare(sql).run();return {subrc:0,dbcnt:Number(x.changes)};}};
 }
 r.phase='load';const context=vm.createContext({abap});for(const o of output.objects){const js=o.chunk.getCode();fs.writeFileSync(out+'/'+o.filename,js);await new vm.Script('(async()=>{'+js+'\n})()',{filename:o.filename}).runInContext(context,{timeout:5000});}r.stages.loaded=true;
 if(c.artifactOnly){r.status='ARTIFACT_TRANSPILED_NO_BEHAVIOR';r.coverage='Transpiler returning does not establish CDS/BDEF semantic execution';return r;}
 const C=abap.Classes.ZCL_R4_CASE;if(!C?.METHODS.RUN)throw Error('HARNESS_METHOD_MISSING');const meta=C.METHODS.RUN;
 r.phase='execute';const inputs=c.reference.length?c.reference:[{input:{},smoke:true}];
 for(const sample of inputs){const args={};for(const [name,p]of Object.entries(meta.parameters).filter(([,p])=>p.parm_kind==='I')){args[name.toLowerCase()]=p.type().set(sample.input[name]??0);}const check={input:sample.input};try{const actual=await new C().run(args);check.actual=actual?.get?actual.get():actual;check.completed=true;if(!sample.smoke){check.expected=sample.expected;check.pass=JSON.stringify(check.actual)===JSON.stringify(sample.expected);}else check.smokeOnly=true;}catch(e){check.completed=false;check.error=String(e.stack||e);}r.checks.push(check);}
 r.stages.invoked=true;r.completed=r.checks.filter(x=>x.completed).length;r.referenceExecuted=r.checks.filter(x=>x.completed&&!x.smokeOnly).length;r.referencePassed=r.checks.filter(x=>x.pass===true).length;
 r.status=r.checks.some(x=>!x.completed)?'EXECUTION_ERROR':r.checks.some(x=>x.pass===false)?'REFERENCE_MISMATCH':c.reference.length?'LOCAL_VERIFIED':'SMOKE_COMPLETED_NO_ORACLE';
}catch(e){r.status='LOCAL_TOOLCHAIN_ERROR';r.error=String(e.stack||e);}finally{if(db)db.close();fs.writeFileSync(out+'/result.json',JSON.stringify(r,null,2));}return r;}
if(require.main===module)run(process.argv[2],process.argv[3]).then(r=>console.log(JSON.stringify({id:r.id,status:r.status,phase:r.phase,checks:r.referencePassed+'/'+r.referenceExecuted,error:r.error?.slice(0,160)}))).catch(e=>{console.error(e);process.exitCode=1;});
module.exports={run};
