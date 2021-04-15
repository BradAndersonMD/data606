import os

def main():
    snippets_dir = 'data\\snippets'
    dest_dir = os.getcwd() + "\\" + snippets_dir + "\\" 
    
    for file in os.listdir(snippets_dir):
        file_name, ext = file.split('.mp4')
        file_name += ".mp3"
        orin_file = dest_dir + file
        dest_file = dest_dir + file_name
        os.system('ffmpeg -i {0} -b:a 192K -vn {1}'.format(orin_file, dest_file))


if __name__ == '__main__':
    main()