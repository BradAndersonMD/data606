import speech_recognition as sr
import os

def main():
    
    snippets = get_snippet_files()
    
    r = sr.Recognizer()
    cwd = os.getcwd()
    transcripts_dir = 'data\\transcripts'
    snippets_dir = 'data\\snippets'
    dest_transcripts = cwd + "\\" + transcripts_dir + "\\"
    #use the audio as the source file
    for snippet in snippets:
        
        flac_snippet = convert_to_flac(snippet)
        flac_file_name = flac_snippet.split("\\")[-1]
        
        #https://github.com/Uberi/speech_recognition/blob/master/examples/audio_transcribe.py
        with sr.AudioFile(flac_snippet) as source:
            audio = r.record(source) # reads the entire audio file
          
        try:
            speech_to_text = r.recognize_sphinx(audio)
            #strip file extenstion
            txt_file_name = flac_file_name.split(".flac")[0]
            with open(dest_transcripts + txt_file_name + ".txt", 'w') as transcript:
                transcript.writelines(speech_to_text)
            
            os.remove(cwd + "\\" + snippets_dir + "\\" + flac_file_name)
            
        except sr.UnknownValueError:
            pass
        except sr.RequestError:
            pass
    
def convert_to_flac(snippet):
    file_name, ext = snippet.split('.mp4')
    file_name += ".flac"
    os.system('ffmpeg -i {0} -vn -ar 22050 -ac:a 64k {1}'.format(snippet, file_name))
    
    return file_name
    
def get_snippet_files():
    snippets = []
    cwd = os.getcwd()
    snippets_dir = 'data\\snippets'
    for file in os.listdir(snippets_dir):
        snippets.append(cwd + "\\" + snippets_dir + "\\" + file)
        
    return snippets
    
if __name__ == '__main__':
    main()