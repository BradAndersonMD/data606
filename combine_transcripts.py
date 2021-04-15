import os

def main():
    
    cwd = os.getcwd()
    transcripts_dir = 'data\\transcripts'
    
    with open(cwd + "\\data\\final_transcript.txt", 'w') as outfile:
        for filename in os.listdir(cwd + "\\" + transcripts_dir):
            with open(cwd + "\\" + transcripts_dir + "\\" + filename) as infile:
                outfile.write(infile.read())
            
            outfile.write("\n")
    
if __name__ == '__main__':
    main()
    
    
    
    