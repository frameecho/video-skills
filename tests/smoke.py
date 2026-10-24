#!/usr/bin/env python3
"""End-to-end synthetic render and negative validation test."""
from pathlib import Path
import os,subprocess,tempfile,json
r=Path(__file__).resolve().parents[1];s=r/'skills/reference-code-mv'
with tempfile.TemporaryDirectory() as d:
 d=Path(d);audio=d/'tone.wav';out=d/'demo.mp4'
 subprocess.run(['ffmpeg','-v','error','-f','lavfi','-i','sine=frequency=440:duration=2',str(audio)],check=True)
 subprocess.run([os.getenv('NODE','node'),str(s/'scripts/render_canvas.cjs'),str(s/'assets/scene.html'),str(out),'2','30',str(audio)],check=True)
 cmd=[os.getenv('PYTHON','python3'),str(s/'scripts/validate_video.py'),str(out),'--duration','2','--fps','30']
 result=subprocess.run(cmd,capture_output=True,text=True,check=True);assert json.loads(result.stdout)['ok']
 bad=cmd.copy();bad[bad.index('--duration')+1]='3';assert subprocess.run(bad,capture_output=True).returncode!=0
 subprocess.run([os.getenv('PYTHON','python3'),str(s/'scripts/inspect_media.py'),str(out),'--out',str(d/'frames'),'--count','3'],check=True)
 assert len(list((d/'frames').glob('*.png')))==3
 print('PASS: render, decode, audio, frame coverage, extraction; wrong duration rejected')
