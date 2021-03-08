import os
from data_classes import VOD

from resemblyzer import preprocess_wav, VoiceEncoder
from resemblyzer.hparams import sampling_rate

def main():
    
    cwd = os.getcwd()
    snippets = '\\data\\snippets\\'
    dest_file_name = cwd + snippets
    vods = get_vods()
    for i, vod in enumerate(vods):
          similarity_dict, wav_splits = get_speaker_similarity_dict_and_wav_splits(vod.get_url())
          slices = get_snippet_time_stamps(similarity_dict, wav_splits)
         
          for j, sli in enumerate(slices):
              print(sli.start, sli.stop)
              f_name = dest_file_name + str(i) + "-" + str(j) + ".mp4"
              os.system('ffmpeg -ss {1} -to {2} -i {0} -vn -ar 22050 -ac 2 -b:a 64k {3}'.format(vod.file(), sli.start, sli.stop, f_name))
    
    
def get_speaker_similarity_dict_and_wav_splits(file_name):
    print('Processing voices for file:', file_name)
    fpath = os.fspath(file_name)
    wav = preprocess_wav(fpath_or_wav=fpath)
            
    speaker_names = ['Phreak', 'Other']
    segments = [[0, 25], [75, 90]]
    encoder = VoiceEncoder('cpu')
    speaker_wavs = [wav[int(s[0] * sampling_rate):int(s[1] * sampling_rate)] for s in segments]
    print("Running the continuous embedding on cpu, this might take a while...")
    _, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=16)
    
    speaker_embeds = [encoder.embed_utterance(speaker_wav) for speaker_wav in speaker_wavs]
    similarity_dict = {name: cont_embeds @ speaker_embed for name, speaker_embed in 
                           zip(speaker_names, speaker_embeds)}
    
    return similarity_dict, wav_splits
    
def get_snippet_time_stamps(similarity_dict, wav_splits):
    #convert the splits to time splits
    times = [((s.start + s.stop ) / 2) / 16000 for s in wav_splits]
    
    phreak_time = []
    for i, time in enumerate(times):
        phreak_confidence = similarity_dict['Phreak'][i]
        other_confidence = similarity_dict['Other'][i]
        #ensure that only Phreak is speaking
        if phreak_confidence > .75 and other_confidence < .75:
            phreak_time.append(time)

    remove_times = []
    for i, j in zip(phreak_time[:-1], phreak_time[1:]):
        diff = j - i
        if (diff > 1.5):
            remove_times.append(i)
            remove_times.append(j)
            
    air_times = list(set(phreak_time) - set(remove_times))
    air_times.sort()
    slices = []
    
    print(air_times)
    start, stop, end = 0, 0, air_times[-1]
    
    for i, j in zip(air_times[:-1], air_times[1:]):
        diff = j - i
        if (diff > 3):
            stop = i
            if(start != stop):
                s = slice(start, stop)
                slices.append(s)
                start = j
    
    s = slice(stop, end)
    slices.append(s)

    return slices        
    
def get_vods():
    vods = []
    cwd = os.getcwd()
    videos = '\\data\\videos\\'
    for file in os.listdir('data/videos'):
        name, time_split = file.split('-t=')
        time, ext = time_split.split('.mp4')
        file_name = cwd + videos + file
        vod = VOD(file_name, time)
        vods.append(vod)
        
    return vods


if __name__ == '__main__':
    main()