# Запуск: python3 add_tracks.py  (из папки сайта). Добавляет в music/tracks.json все новые mp3 из папки music.
import os,json,re,struct
D=os.path.dirname(os.path.abspath(__file__));M=os.path.join(D,'music');C=os.path.join(M,'covers');J=os.path.join(M,'tracks.json')
os.makedirs(C,exist_ok=True)
lst=json.load(open(J,encoding='utf-8')) if os.path.exists(J) else []
have={x['f'] for x in lst}
def ss(b):return(b[0]&127)<<21|(b[1]&127)<<14|(b[2]&127)<<7|(b[3]&127)
def dec(b,e):
    try:
        if e==0:
            try:return b.decode('cp1251').strip('\x00 ')
            except:return b.decode('latin1').strip('\x00 ')
        return (b.decode('utf-8','ignore') if e==3 else b.decode('utf-16','ignore')).strip('\x00 ')
    except:return ''
def read(p):
    d=open(p,'rb').read(6*1024*1024);m={}
    if d[:3]!=b'ID3':return m
    v=d[3];end=min(len(d),10+ss(d[6:10]));q=10
    while q+10<end:
        fid=d[q:q+4].decode('latin1')
        fs=ss(d[q+4:q+8]) if v==4 else struct.unpack('>I',d[q+4:q+8])[0]
        if not fs or q+10+fs>len(d):break
        b=d[q+10:q+10+fs]
        if fid=='TIT2':m['title']=dec(b[1:],b[0])
        if fid=='TPE1':m['artist']=dec(b[1:],b[0])
        if fid=='APIC':
            e=b[0];k=1
            while b[k]:k+=1
            k+=2
            if e in(1,2):
                while b[k] or b[k+1]:k+=2
                k+=2
            else:
                while b[k]:k+=1
                k+=1
            m['pic']=b[k:]
        q+=10+fs
    return m
new=0
for f in sorted(os.listdir(M)):
    if not f.lower().endswith('.mp3') or 'music/'+f in have:continue
    m=read(os.path.join(M,f));base=os.path.splitext(f)[0]
    t=m.get('title') or re.sub(r'[_\-]+',' ',base).strip();c=None
    if m.get('pic') and len(m['pic'])>200:
        ext='png' if m['pic'][:4]==b'\x89PNG' else 'jpg'
        open(os.path.join(C,base+'.'+ext),'wb').write(m['pic']);c='music/covers/%s.%s'%(base,ext)
    lst.append({'f':'music/'+f,'t':t,'a':m.get('artist',''),'c':c});new+=1;print('+',m.get('artist',''),'-',t)
json.dump(lst,open(J,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
print('Добавлено новых треков:',new)
