#!/usr/bin/env python3
"""Decode and check a finished MV. Prints JSON and exits nonzero on failure."""
import argparse,json,re,subprocess

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--duration',type=float,required=True);p.add_argument('--fps',type=float,required=True);p.add_argument('--silent',action='store_true');p.add_argument('--allow-tail-black',type=float,default=0);a=p.parse_args()
 if a.duration<=0 or a.fps<=0 or a.allow_tail_black<0:p.error('duration/fps must be positive and black allowance nonnegative')
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_format','-show_streams','-of','json',a.input]))
 errors=[];videos=[s for s in probe['streams'] if s['codec_type']=='video'];audios=[s for s in probe['streams'] if s['codec_type']=='audio']
 if not videos:errors.append('missing video')
 v=videos[0] if videos else {};actual=float(probe['format']['duration']);tol=1/a.fps+.06
 if abs(actual-a.duration)>tol:errors.append('duration mismatch')
 if v.get('pix_fmt')!='yuv420p':errors.append('pixel format must be yuv420p')
 if v.get('codec_name')!='h264':errors.append('video codec must be h264')
 rate=v.get('avg_frame_rate','0/1');num,den=map(float,rate.split('/'));actual_fps=num/den if den else 0
 if abs(actual_fps-a.fps)>.01:errors.append('fps mismatch')
 if abs(int(v.get('nb_read_frames',0))-__import__('math').ceil(a.duration*a.fps))>0:errors.append('decoded frame count mismatch')
 if not a.silent:
  if not audios:errors.append('missing audio')
  elif abs(float(audios[0].get('duration',actual))-a.duration)>tol:errors.append('audio duration mismatch')
 decode=subprocess.run(['ffmpeg','-hide_banner','-v','info','-xerror','-i',a.input,'-vf','blackdetect=d=0.1:pix_th=0.08','-f','null','-'],capture_output=True,text=True)
 if decode.returncode:errors.append('full decode failed')
 black=[]
 for start,end,duration in re.findall(r'black_start:([\d.]+) black_end:([\d.]+) black_duration:([\d.]+)',decode.stderr):
  start,end,duration=map(float,(start,end,duration));allowed=end>=actual-tol and duration<=a.allow_tail_black
  black.append(dict(start=start,end=end,duration=duration,allowed=allowed))
  if not allowed:errors.append('unexpected black interval')
 print(json.dumps(dict(ok=not errors,duration=actual,frames=v.get('nb_read_frames'),fps=actual_fps,black=black,errors=errors),indent=2));return bool(errors)
if __name__=='__main__':raise SystemExit(main())
