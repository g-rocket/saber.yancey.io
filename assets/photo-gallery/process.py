import os, subprocess, io

def get_size(dim, maxw, maxh):
    if dim[0]/dim[1] < maxw/maxh:
        return (dim[0]*maxh/dim[1], maxh)
    else:
        return (maxw, dim[1]*maxw/dim[0])

def get_dim(f):
    return [int(d) for d in
            subprocess.run(['ffprobe',
                    '-show_entries','stream=width,height','-of','default=noprint_wrappers=1:nokey=1',
                    '-i', f], check=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, encoding='utf-8').stdout.strip().split('\n')]

basedir = 'assets/photo-gallery'

os.chdir(os.path.join(os.path.dirname(__file__), '../..'))
files = [f for f in os.listdir(basedir) if not f.endswith('.py') and os.path.isfile(os.path.join(basedir, f))]

with io.StringIO() as s:
    for f in reversed(sorted(files)):
        full = os.path.join(basedir, f)
        thumb = os.path.join(basedir, 'thumbs', f)
        subprocess.run(['ffmpeg', '-y', '-i', full, '-vf', 'scale=800:600:force_original_aspect_ratio=decrease', thumb], check=True)
        #w,h = get_size(get_dim(f), 800,600)
        w,h = get_dim(thumb)
        s.write(f'        <a href="{full}"><img width="{round(w)}" height="{round(h)}" src="{thumb}" /></a>\n')
    s.seek(0)
    print(s.read(), end='')