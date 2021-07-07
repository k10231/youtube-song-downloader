import pafy,os,sys,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from ffmpy import FFmpeg

def main():

    destDirExists()
    urlBase = 'https://www.youtube.com' #Baseurl
    xpath = '//*[@id="thumbnail"]'
    #Setting options for chromedriver
    options = Options()
    #split arguments if needed
    options.add_argument('--headless --mute-audio')

    #Init chromedriver
    driver = webdriver.Chrome('chromedriver.exe',chrome_options=options)
    #Init counter variable for loop
    counter = 0

    #Variable for while loop, taken from args
    #check first arg to be INT
    try:
        counterLimit = int(sys.argv[1])
    except:
        throwError()
        #Check if there is enough args and second argument is string
    if len(sys.argv) != 3 or type(sys.argv[2]) is not str:
        throwError()

    else:
        #setting full url
        url = urlBase + sys.argv[2]
        driver.get(url)
        #Starting mainloop
        while(counterLimit > counter):
            video = pafy.new(url)
            #New pafy-object,
            title = editTitle(video.title)

            found = isFileInDir(title)
            #Checking is file in directory, setting found = true if exists
            if not found:
                #Taking only audio from pafy-object
                audio = video.getbestaudio()

                #taking song files extension. Its needed for ffmpeg object to convert
                fileExtension = audio.extension
                #Making full song name
                songName = title+'.'+fileExtension
                #download song and giving it correct filename
                try:
                    audio.download(songName, quiet=True)
                except:
                    pass

                audioConverter = FFmpeg(inputs={songName:None}#Converting downloaded file to .mp3
                ,outputs={os.getcwd()+'\\mp3\\'+title+'.mp3':None})
                try:
                    audioConverter.run()
                except IOError as e:
                    print('I/O error: '+e.errno+' '+ e.strerror)
                os.remove(songName) #remove original file from directory
                print(songName + ' Download complete!')
                counter +=1 #Incrementing counter

            #Giving chromedriver xpath to find youtubes recommend song for next file to download. And calling
            #Click() for simulating mouseclick.
            driver.find_element_by_xpath(xpath).click()
            #When moved to new site inside chromedriver, we get current url and set it to url for next round.
            url = driver.current_url



    driver.quit() #Quitting chromedriver

def destDirExists():
    if not os.path.isdir(os.getcwd()+'\mp3'):
        os.mkdir('mp3')

#Removing not wanted characters from title and removing text inside parentheses () and []
def editTitle(title):
    chars = ':?|;"'
    title = title.replace(title[title.find('['):title.rfind(']')+1],'').replace(title[title.find('('):title.rfind(')')+1],'')
    for c in chars:
        if c in title:
            title = title.replace(c,'')
    return title

#Check if file is already in directory,returning boolean
def isFileInDir(title):
    found = False
    for item in os.listdir(os.getcwd()+'\\mp3\\'):
        if replaceSigns(item.rsplit('.',1)[0]) == replaceSigns(title):
            print(title + '. Already in directory. Moving to next song.')
            found = True
    return found


#Removes all whitespaces and signs from string for comparing filename and title
def replaceSigns(string):
     return ''.join(e for e in string if e.isalnum())


def throwError():
    print("\nIncorrect arguments. Give number how many times you wanna run download and then url where to start!")
    print("Ex. >> ytdownloader 2 /watch?v=n024i5lj5\n")
    sys.exit()

if __name__ == '__main__':
    main()
