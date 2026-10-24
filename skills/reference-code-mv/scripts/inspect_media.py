#!/usr/bin/env python3
"""Probe a local video and extract evenly distributed timestamped frames."""
import argparse,json,subprocess
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('input');p.add_argument('--out',required=True);p.add_argument('--count',type=int,default=12);a=p.parse_args()
 if a.count<1:p.error('--count must be positive')
 probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_format','-show_streams','-of','json',a.input]))
 duration=float(probe['format']['duration']);out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 if (out/'media.json').exists():p.error('Output metadata exists; choose a fresh directory')
 (out/'media.json').write_text(json.dumps(probe,ensure_ascii=False,indent=2))
 for i in range(a.count):
  t=duration*(i+.5)/a.count
  subprocess.run(['ffmpeg','-v','error','-n','-ss',str(t),'-i',a.input,'-frames:v','1',str(out/f'{i:03d}-{t:.3f}s.png')],check=True)
 print(out)
if __name__=='__main__':main()
