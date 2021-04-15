from google.cloud import speech, storage
from threading import Thread


def main():
    
    vods = get_vods()
    gs_prefix = "gs://full-15min-vods/"

    for vod in vods:
        print('Starting new thread...')
        thread = Thread(target = transcribe, args=(gs_prefix, vod))
        thread.start()    
    

def transcribe(gs_prefix, vod):
    '''
    This is an async call to google clouds long running speech recognize
    '''

    gcs_uri = gs_prefix + vod
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=44100,
        language_code="en-US",
    )
    
    operation = client.long_running_recognize(config=config, audio=audio)
    print('Running transcription for vod:', vod)
    print("Waiting for operation to complete...")
    response = operation.result(timeout=3600)
    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    with open(r"D:\\Users\\Brad\\Graduate_School\\2021\\data606\\data\\transcripts\\" + vod + '.txt', 'w') as openfile:
        
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            transcript = result.alternatives[0].transcript
            print(u"Transcript: {}".format(transcript))
            openfile.writelines(transcript)
            


def get_vods():
    storage_client = storage.Client()
    blobs = storage_client.list_blobs("full-15min-vods")
    vods = []
    
    for blob in blobs:
        vods.append(blob.name)
            
    return vods
    
if __name__ == '__main__':
    main()