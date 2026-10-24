#!/usr/bin/env node
const fs=require('node:fs'), path=require('node:path'), {pathToFileURL}=require('node:url');
const {spawn}=require('node:child_process'), {once}=require('node:events');
async function main(){
 const [html,out,d,f,audio]=process.argv.slice(2), duration=Number(d),fps=Number(f);
 if(!out||!Number.isFinite(duration)||duration<=0||!Number.isFinite(fps)||fps<=0)throw Error('Usage: node render_canvas.cjs scene.html output.mp4 duration fps [audio]');
 if(fs.existsSync(out)||fs.existsSync(out+'.manifest.json'))throw Error('Output already exists');
 const source=path.resolve(html);fs.accessSync(source);if(audio)fs.accessSync(audio);
 let pw;try{pw=require(process.env.PLAYWRIGHT_MODULE||'playwright')}catch(e){pw=require(require.resolve('playwright',{paths:[process.cwd()]}))}
 const browser=await pw.chromium.launch({headless:true,...(process.env.BROWSER_EXECUTABLE?{executablePath:process.env.BROWSER_EXECUTABLE}:{})});
 let enc;
 try{
 const page=await browser.newPage();await page.goto(pathToFileURL(source).href);
 await page.evaluate(async()=>{await document.fonts.ready;await window.ready;if(typeof window.renderFrame!=='function')throw Error('Missing renderFrame(t)')});
 const size=await page.evaluate(()=>({width:window.VIDEO_WIDTH,height:window.VIDEO_HEIGHT}));
 if(!Number.isInteger(size.width)||!Number.isInteger(size.height)||size.width<=0||size.height<=0||size.width%2||size.height%2)throw Error('Declare positive even VIDEO_WIDTH and VIDEO_HEIGHT');
 await page.setViewportSize(size);
 fs.mkdirSync(path.dirname(path.resolve(out)),{recursive:true});
 const args=['-hide_banner','-loglevel','error','-n','-f','image2pipe','-framerate',String(fps),'-vcodec','png','-i','pipe:0'];
 if(audio)args.push('-i',path.resolve(audio));
 args.push('-map','0:v:0');if(audio)args.push('-map','1:a:0','-c:a','aac','-b:a','320k','-af',`apad=whole_dur=${duration}`);
 args.push('-c:v','libx264','-vf','scale=in_range=pc:out_range=tv','-pix_fmt','yuv420p','-color_range','tv','-t',String(Math.ceil(duration*fps)/fps),'-movflags','+faststart',out);
 enc=spawn('ffmpeg',args,{stdio:['pipe','inherit','inherit']});
 const ended=new Promise((resolve,reject)=>{enc.on('error',reject);enc.on('close',code=>code===0?resolve():reject(Error('FFmpeg exit '+code)))});
 // Attach rejection handler immediately, then await the original promise below.
 ended.catch(()=>{});let pipeError;enc.stdin.on('error',e=>{pipeError=e});
 const frames=Math.ceil(duration*fps);
 for(let i=0;i<frames;i++){
 if(pipeError)throw pipeError;
 await page.evaluate(t=>window.renderFrame(t),i/fps);
 const png=await page.locator('canvas').screenshot({type:'png'});
 if(!enc.stdin.write(png))await Promise.race([once(enc.stdin,'drain'),ended.then(()=>{throw Error('Encoder ended before all frames')})]);
 }
 enc.stdin.end();await ended;
 fs.writeFileSync(out+'.manifest.json',JSON.stringify({duration,fps,frames,width:size.width,height:size.height,complete:true},null,2)+'\n');
 console.log(`Rendered ${frames} frames to ${out}`);
 }finally{if(enc&&enc.exitCode===null)enc.kill();await browser.close()}
}
main().catch(e=>{console.error(e.message);process.exitCode=1});
