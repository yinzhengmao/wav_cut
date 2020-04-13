from pydub import AudioSegment
from pydub.silence import split_on_silence
import os
import argparse

def main(input_wav):
    audiopath = input_wav
    audiotype = 'wav' 
    print('读入音频')
    sound = AudioSegment.from_file(audiopath, format=audiotype)
    print('开始分割')
    # min_silence_len: 拆分语句时，静默满0.3秒则拆分。silence_thresh：小于-51dBFS以下的为静默。
    chunks = split_on_silence(sound,min_silence_len=400,silence_thresh=-37,keep_silence=200)
    print(len(chunks[0]))
    # 放弃长度小于0.4秒的录音片段
    abandon_chunk_len = 400
    for i in list(range(len(chunks)))[::-1]:
        if len(chunks[i]) <= abandon_chunk_len:
            chunks.pop(i)
        print('取有效分段：', len(chunks))
                
    (filepath,tempfilename) = os.path.split(audiopath)
    (filename,extension) = os.path.splitext(tempfilename)
    chunks_path = filepath+'/chunk1s/'
    if not os.path.exists(chunks_path):os.mkdir(chunks_path)

    print('开始保存')
    for i in range(len(chunks)):
        new = chunks[i]
        save_name = chunks_path+filename+'_'+'%04d.%s'%(i,audiotype) 
        new.export(save_name, format=audiotype)
        #print(save_name,len(new))
        print('%04d'%i,len(new))
    print('保存完毕')

if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='split data')
    parser.add_argument('--input-dir', type=str,
                    help='Input wav directory')
    args = parser.parse_args()
    input_file_dir= args.input_dir
    main(input_file_dir)