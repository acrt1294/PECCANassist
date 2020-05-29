


######################################################################################################################## selenium

####################################
#######      packages      #########
####################################

import textwrap
from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import re

####################################
#######  open the browser  #########
####################################

keys=''
while keys=='':
    try:
        phageName = str(input('Please input the name of the phage you are looking for:\n'))
        browser = webdriver.Firefox(executable_path='C:\\Users\\acrt1\\Desktop\\drivers\\geckodriver-v0.26.0-win64\\geckodriver.exe')
        browser.get('https://phagesdb.org/')
        keys=0
    except Exception as e:
        browser.quit()
        e = textwrap.fill(str(e),width=70)
        print('That\'s wierd, somethingwent wrong!\n\nERROR REPORT:\n',e)
        keys = 0

        minikeys=''
        while minikeys == '':
            Y_N = input('\nWant to try again? [y/n]\nUSER INPUT: ')
                # loops until the user enters either 'y' or 'n'
            keys_Y_N_option = ''
            while keys_Y_N_option == '':
                try:
                    if Y_N == 'y':
                        keys_Y_N_option=0
                        minikeys = 0
                        print('')
                    elif Y_N == 'n':
                        print('\n\nTerminating process')
                        minikeys=0
                        keys=0
                        keys_Y_N_option=0
                        time.sleep(5)
                        exit(0)
                    else:
                        print('\nPlease try to enter either \'y\' or \'n\' next time. Let\'s try again!')
                        keys_Y_N_option = 0
                except Exception as e:
                    continue

# gets you to your phage's page
browser.minimize_window()
searchBar = browser.find_element_by_id('directToPhage')
searchBar.send_keys(phageName)
searchBar.send_keys(Keys.ENTER)

####################################
##   creating a beautiful soup    ##
####################################

time.sleep(5)
phagePage_URL = browser.current_url
print('\nReference Page URL:')
print(phagePage_URL)
print('')

# name as stored in url, used in finding and scraping gene links
phageName_URL = re.search('(/){1}(\w)+(/){1}(?!.)',phagePage_URL)
phageName_URL = re.sub('(/)','',phageName_URL.group())

phagePage = requests.get(phagePage_URL)
phagePage_conent = phagePage.content
phagePage_soup = BeautifulSoup(phagePage_conent,'lxml')

# fetch all links to later search for the relevant links in this list
links = phagePage_soup.find_all('a')

# create a list with the relevant links
geneLinkList = []
for link in links[::-1]:
    geneURL = link.attrs['href']
    if '/genes/' in geneURL:
        geneLinkList.append(geneURL)

######################################
'             functions              '
######################################


# opens the page for a particular gene and returns it's amino acid sequence
def gene_page_opener(geneURL):

    #URL construction
    genePage_URL = 'https://phagesdb.org'+geneURL

    # get page
    genePage = requests.get(genePage_URL)
    genePage_content = genePage.content
    soup = BeautifulSoup(genePage_content, 'lxml')

    # fetch aminoacid sequence
    aa = soup.find(id='aaSequence')
    aa = str(aa.contents[0])

    return aa

# opens either all available genemarks or the main one on new windows. returns browser as genemarkBrowser
"""" STATUS: NEEDS TESTING """
def genemarkAssistant(phagePage):

    page = requests.get(phagePage_URL)
    pg_content = page.content
    soup = BeautifulSoup(pg_content, 'lxml')
    # fetch all links to later search for the relevant links in this list
    links = soup.find_all('a')
    # create a list with the relevant links
    genemarkLinkList = []
    for link in links[::]:
        genemarkURL = link.attrs['href']
        if 'genemark' in genemarkURL:
            genemarkLinkList.append(genemarkURL)
    # open a new window with one of the genemark reports
    genemarkBrowser = webdriver.Firefox(
        executable_path='C:\\Users\\acrt1\\Desktop\\drivers\\geckodriver-v0.26.0-win64\\geckodriver.exe')
    genemarkBrowser.get('https://phagesdb.org'+genemarkLinkList[0])
    # open new tabs with
    for url in genemarkLinkList[1::]:
        keys = ''
        while keys == '':
            try:
                argument = ('window.open(\'') +'https://phagesdb.org'+ url + ('\'), \'new window\'')
                argument = str(argument)
                genemarkBrowser.execute_script(argument)
                genemarkBrowser.minimize_window()
                keys = 0

            # error handling
            except Exception as e:
                #genemarkBrowser.quit()
                e = textwrap.fill(str(e), width=70)
                print('That\'s wierd, somethingwent wrong!\n\nERROR REPORT:\n', e)

                # highlight the coordinate you're looking for
                # coming soon

                minikeys = ''
                while minikeys == '':
                    Y_N = input('\nWant to try again? [y/n]\nUSER INPUT: ')
                    # loops until the user enters either 'y' or 'n'
                    keys_Y_N_option = ''
                    while keys_Y_N_option == '':
                        try:
                            if Y_N == 'y':
                                keys_Y_N_option = 0
                                minikeys = 0
                                print('')
                            elif Y_N == 'n':
                                print('\n\nTerminating process')
                                minikeys = 0
                                keys = 0
                                keys_Y_N_option = 0
                                time.sleep(5)
                                exit(0)
                            else:
                                print('\nPlease try to enter either \'y\' or \'n\' next time. Let\'s try again!')
                                keys_Y_N_option = 0
                        except Exception as e:
                            continue
    return genemarkBrowser

# Creates alignment browser. Returns browser as alignmentBrowser.
def createAlignmentBrowser(geneURL):
    ######### open blast window
    # URL construction
    genePage_URL = 'https://phagesdb.org'+geneURL
    keys = ''
    while keys == '':
        try:
            alignmentBrowser = webdriver.Firefox(
                executable_path='C:\\Users\\acrt1\\Desktop\\drivers\\geckodriver-v0.26.0-win64\\geckodriver.exe')
            alignmentBrowser.get(genePage_URL)
            keys = 0
        except Exception as e_:
            try:
                alignmentBrowser.quit()
            except:
                ''
            e_ = textwrap.fill(str(e_), width=70)
            print('That\'s wierd, somethingwent wrong!\n\nERROR REPORT:\n', e_)
            input('Press ENTER to continue!')

            minikeys = ''
            while minikeys == '':
                Y_N = input('\nWant to try again? [y/n]\nUSER INPUT: ')
                # loops until the user enters either 'y' or 'n'
                keys_Y_N_option = ''
                while keys_Y_N_option == '':
                    try:
                        if Y_N == 'y':
                            keys_Y_N_option = 0
                            minikeys = 0
                            print('')
                        elif Y_N == 'n':
                            print('\n\nTerminating process')
                            minikeys = 0
                            keys = 0
                            keys_Y_N_option = 0
                            time.sleep(5)
                            exit(0)
                        else:
                            print('\nPlease try to enter either \'y\' or \'n\' next time. Let\'s try again!')
                            keys_Y_N_option = 0
                    except Exception as e:
                        continue
    return alignmentBrowser

# opens an hhpred tab on allignment window and runs it, also generates a report of its findings
def HHPredAssistant(alignmentBrowser,aminosequence):


    """ STATUS: NEEDS DEBUGGING """
    def HHpredSetUp():

        # returns Y_N ('y' or 'n') for USING DEFAULT SETTINGS.
        # If 'y' use default settings. If 'n' pop up window for user to change them.
        def Y_N():
            # Augusto Romero 4/19/2020

            # Change (A) , (B) and (C) lines

            ###### parenchyme
            #import time
            #import textwrap
            ######  mesenchyme

            # sets up loop for y/n data entry
            minikeys = ''
            while minikeys == '':

                # Y/N question prompt
                ################### change the line below this comment #####################  (A)
                Y_N = input('\nWould you like to use the default settings for HHpred? [y/n]\nUSER INPUT: ')

                # loops until the user enters either 'y' or 'n'
                keys_Y_N_option = ''
                while keys_Y_N_option == '':
                    try:
                        if Y_N == 'y':
                            # add additional key if necessary
                            ################### consider changing the commented line below this comment #####################  (B)
                            # additional key = 0
                            keys_Y_N_option = 0
                            minikeys = 0
                            print('')
                        elif Y_N == 'n':
                            # add additional key if necessary
                            ################### consider changing the commented line below this comment #####################  (C)
                            # additional key = 0
                            minikeys = 0
                            keys_Y_N_option = 0

                        else:
                            print('\nPlease try to enter either \'y\' or \'n\' next time. Let\'s try again!')
                            keys_Y_N_option = 0
                    except Exception as e_:
                        print('Something went wrong! Generating error report:\n')
                        e_ = textwrap.fill(e, width=70)
                        print('Error Report:\n', e_)
                        input('\nPress ENTER to continue.\n')
                        continue

            return Y_N

        # uses default settings or sends you to
        # keys=''
        # while keys == '':
        #     try:
                #
                #time.sleep(1)
                #alignmentBrowser.switch_to.window(browser.window_handles[-1])
                #
                #alignmentBrowser.minimize_window()
                #Y_N = Y_N()
                #alignmentBrowser.maximize_window()
                #if Y_N == 'y':
                #     keys=0
                #     return
                #
                # if Y_N == 'n':
                #     print('\n',textwrap.fill('Please change the settings to your liking. '
                #                              'The relevant browser window is being called!',width=70))
                #     print('NOTE: please minimize the window after you are done')
                #     input('Press Enter to continue.\n')
                #     alignmentBrowser.maximize_window()
                #     input('Press Enter to continue after you are done editing the settings.\n')
            #         keys = 0
            #
            #         # open hhpred
            #         try:
            #             alignmentBrowser.execute_script("window.open('https://toolkit.tuebingen.mpg.de/tools/hhpred');")
            #             tabs = browser.window_handles
            #             alignmentBrowser.switch_to.window(tabs[-1])
            #         except Exception as e:
            #             print('\nTimeOut error. Check your internet connection!')
            #             input('Press ENTER to continue.')
            #
            #
            # except Exception as e:
            #
            #     print('Something went wrong! Generating error report:\n')
            #     #e = textwrap.fill(e, width=70)
            #     print('Error Report:\n', e)

    HHpredSetUp()
    """   STATUS: NEEDS DEBUGGING """
    def alignment_initiation(aminoseq):
        keys = ''
        while keys == '':
            try:
                # open hhpred
                try:
                    alignmentBrowser.execute_script("window.open('https://toolkit.tuebingen.mpg.de/tools/hhpred');")
                except Exception as e:
                    print('failed to open HHpred tab.')
                    continue

                try:
                    tabs = alignmentBrowser.window_handles
                    alignmentBrowser.switch_to.window(tabs[-1])
                    time.sleep(8)
                except Exception as e:
                    print('\nTimeOut error. Check your internet connection!')
                    input('Press ENTER to continue.')

                # introduces the sequence and aligns it
                try:
                    wait = WebDriverWait(alignmentBrowser,20)
                    try:
                        sequenceBox = wait.until(ec.element_to_be_clickable((By.XPATH,'//*[@id="__BVID__121"]')))
                    except Exception as e:
                        ''
                    sequenceBox = wait.until(ec.element_to_be_clickable((By.ID, '__BVID__121')))

                except Exception as e:
                    try:
                        sequenceBox = alignmentBrowser.find_element_by_class_name("textarea-alignment break-all form-control")
                    except Exception as e:
                        try:
                            sequenceBox = alignmentBrowser.find_element_by_id('__BVID__121')
                        except Exception as e:
                            try:
                                sequenceBox = alignmentBrowser.find_element_by_xpath('//*[@id="__BVID__121"]')
                            except Exception as e:
                                sequenceBox = alignmentBrowser.find_element_by_css_selector('#__BVID__121')

                sequenceBox.send_keys(aminoseq)

                # presses go button
                #time.sleep(5)

                try:
                    cookie_banner =( WebDriverWait(alignmentBrowser, 10).until(
                            ec.element_to_be_clickable((By.CLASS_NAME, 'Cookie__button')))
                                    )
                    cookie_banner.click()
                except Exception as e:
                    ''
                try:

                    goButton = (
                        WebDriverWait(alignmentBrowser, 10).until(ec.element_to_be_clickable(
                        (By.XPATH,'/html/body/div/div[1]/div[3]/div[2]/div/form/div/div/div[2]/div[1]/fieldset/div/button')))
                    )

                except Exception as e:
                    try:
                        goButton = alignmentBrowser.find_element_by_class_name("btn submit-button btn-primary")
                        p=1
                    except Exception as e:
                        try:
                            goButton = alignmentBrowser.find_element_by_partial_link_text('Submit')
                            p=1
                        except Exception as e:
                            alignmentBrowser.minimize_window()
                            print('Failed to submit HHpred. Press enter to submit manually.')
                            input('Press ENTER to continue.')

                try:
                    goButton.click()
                except Exception as e:
                    try:
                        goButton.click()
                        p=1
                    except Exception as e:
                         pass
                    # try:
                    #     time.sleep(1)
                    #     goButton.click()
                    # except Exception as e:
                    #     try:
                    #         time.sleep(1)
                    #         goButton.click()
                    #     except Exception as e:
                    #         try:
                    #             form = alignmentBrowser.find_element_by_class_name('tool-form')
                    #             form.submit()
                    #             p=1
                    #             #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
                    #         except Exception as e:
                    #             print('failure to press HHpred submit')
                # if you get to this point, you were successful so we unlock the key
                keys = 0

            # error handling
            except Exception as e:
                e = textwrap.fill(str(e), width=70)
                print('That\'s wierd, something went wrong!\n\nERROR REPORT:\n', e)
                #input('Press ENTER to continue')

                # highlight the coordinate you're looking for
                # coming soon

                minikeys = ''
                while minikeys == '':
                    Y_N = input('\nWant to try again? [y/n]\nUSER INPUT: ')
                    # loops until the user enters either 'y' or 'n'
                    keys_Y_N_option = ''
                    while keys_Y_N_option == '':
                        try:
                            if Y_N == 'y':
                                keys_Y_N_option = 0
                                minikeys = 0
                                print('')
                            elif Y_N == 'n':
                                print('\n\nTerminating process')
                                minikeys = 0
                                keys = 0
                                keys_Y_N_option = 0
                                time.sleep(5)
                                exit(0)
                            else:
                                print('\nPlease try to enter either \'y\' or \'n\' next time. Let\'s try again!')
                                keys_Y_N_option = 0
                        except Exception as e:
                            print('\Something went wrong! Let\'s try again\n')
                            input('Press enter to continue')
                            continue
    alignment_initiation(aminosequence)



# blasts on ncbi and phages db and opens starterator
def blast_assistant(alignmentBrowser):

    def starterator():

        try:
            tabs = alignmentBrowser.window_handles
            alignmentBrowser.switch_to.window(tabs[0])
            time.sleep(1)
                                                                      #/html/body/div/div[3]/div[2]/div[2]/table[1]/tbody/tr[5]/td[2]/strong/a

            # clicks starterator link in phage page
            starterator_link = alignmentBrowser.find_element_by_xpath('/html/body/div/div[3]/div[2]/div[2]/table[1]/tbody/tr[5]/td[2]/strong/a')
            try:
                starterator_link = WebDriverWait(alignmentBrowser,10).\
                    until(ec.element_to_be_clickable(
                    (By.XPATH, '/html/body/div/div[3]/div[2]/div[2]/table[1]/tbody/tr[5]/td[2]/strong/a')))
            except Exception as e:
                try:
                    starterator_link = WebDriverWait(alignmentBrowser,10)\
                        .until(ec.presence_of_element_located(
                        (By.CSS_SELECTOR,
                         '.phamStats > tbody:nth-child(1) > tr:nth-child(5) > '
                         'td:nth-child(2) > strong:nth-child(1) > a:nth-child(1)')))
                except:
                    try:
                        starterator_link = alignmentBrowser.find_element_by_xpath(
                        '/html/body/div/div[3]/div[2]/div[2]/table[1]/tbody/tr[5]/td[2]/strong/a')
                    except:
                        ''#starterator_link = alignmentBrowser.find_element_by_partial_link_text()

            starterator_URL = starterator_link.get_attribute('href')
            alignmentBrowser.execute_script(('window.open(\'') + starterator_URL + ('\'), \'new window\''))

            # clicks ncbi blast button in ncbi page
            tabs = alignmentBrowser.window_handles
            alignmentBrowser.switch_to.window(tabs[1])

        except Exception as e:
            alignmentBrowser.minimize_window()
            print('\nThe program failed to detect the relevant button (starterator link). Please press it manually\nNOTE: some genes might not have a starterator report.\n')
            #input('Press ENTER to continue.\n')
            #alignmentBrowser.maximize_window()

    starterator()

    """  STATUS: needs debugging """
    def ncbi_blast_subroutine():
    #alignmentBrowser.find_element_by_class_name('blastme blueButton')
    #alignmentBrowser.find_element_by_partial_link_text('')
    #alignmentBrowser.find_elements_by_class_name('')


        try:
            tabs = alignmentBrowser.window_handles
            alignmentBrowser.switch_to.window(tabs[0])
            time.sleep(1)

            # clicks ncbi link in phage page
            button_BlastPhagesDB_NCBI = alignmentBrowser.find_element_by_partial_link_text('NCBI')
            ncbi_URL = button_BlastPhagesDB_NCBI.get_attribute('href')
            alignmentBrowser.execute_script(('window.open(\'') + ncbi_URL + ('\'), \'new window\''))

            # clicks ncbi blast button in ncbi page
            tabs = alignmentBrowser.window_handles
            alignmentBrowser.switch_to.window(tabs[1])
            try:
                blastButton = WebDriverWait(alignmentBrowser, 14).until(
                    ec.element_to_be_clickable((By.ID, 'blastbutton')))
                blastButton.click()

            except Exception as e:
                try:
                    alignmentBrowser.refresh()
                    time.sleep(7)
                    blastButton = alignmentBrowser.find_element_by_id('b1')
                    blastButton.click()
                except Exception as e:
                    alignmentBrowser.minimize_window()
                    print('\nThe program failed to detect the relevant button (blast button on NCBI page). Please press it manually.')
                    input('Press ENTER to continue.\n')
                    alignmentBrowser.maximize_window()
                    input('Hopefully, you managed to blast successfully! \nPress ENTER to continue.\n')

        except Exception as e:
            alignmentBrowser.minimize_window()
            print('\nThe program failed to detect the relevant button (blue blast button on phagesdb). Please press it manually.')
            input('Press ENTER to continue.\n')
            alignmentBrowser.maximize_window()

    ncbi_blast_subroutine()

    def phagesdb_blast_subroutine():
        try:
            tabs = alignmentBrowser.window_handles
            alignmentBrowser.switch_to.window(tabs[0])
            time.sleep(1)
            try:
                try:
                    button_BlastPhagesDB = WebDriverWait(browser,10).until(ec.element_to_be_clickable(
                        (By.PARTIAL_LINK_TEXT,'on PhagesDB')))
                except Exception as e:
                    alignmentBrowser.refresh()
                    button_BlastPhagesDB = WebDriverWait(browser, 10).until(ec.element_to_be_clickable(
                        (By.PARTIAL_LINK_TEXT, 'on PhagesDB')))
            except Exception as e:
                button_BlastPhagesDB = alignmentBrowser.find_element_by_partial_link_text('on PhagesDB')
            button_BlastPhagesDB_URL = button_BlastPhagesDB.get_attribute('href')
            alignmentBrowser.execute_script(('window.open(\'') + button_BlastPhagesDB_URL + ('\'), \'new window\''))

            # clicks ncbi blast button in ncbi page
            tabs = alignmentBrowser.window_handles
            alignmentBrowser.switch_to.window(tabs[1])
            time.sleep(2.5)

            alignmentBrowser.find_element_by_name('MainBlastForm').submit()
        except Exception as e:
            try:
                alignmentBrowser.refresh()
                time.sleep(8)
                alignmentBrowser.find_element_by_name('MainBlastForm').submit()

                try:
                    phagesdb_blastbtn = WebDriverWait(alignmentBrowser,5).until(ec.element_to_be_clickable(By.XPATH('/html/body/div/div[3]/div[2]/div[3]/form/input[3]')))
                    phagesdb_blastbtn.click()
                except Exception as e:
                    ''

            except Exception as e:
                alignmentBrowser.minimize_window()
                print('\nThe program failed to detect the button (local blast submission button at phages db). Please press it manually.')
                input('Press ENTER to continue.\n')
                alignmentBrowser.maximize_window()
    phagesdb_blast_subroutine()


    try:
        tabs = alignmentBrowser.window_handles
        alignmentBrowser.switch_to.window(tabs[1])
        alignmentBrowser.close()
    except Exception as e:
        p=1
    try:
        tabs = alignmentBrowser.window_handles
        alignmentBrowser.switch_to.window(tabs[0])
    except Exception as e:
        p=1


######################################################################################################################## GUI




######################################################################################################################## function calling

# calls all the functions the selenium functions that need to be executed
def functionCaller(geneURL):
    aa = gene_page_opener(geneURL)
    alignmentBrowser = createAlignmentBrowser(geneURL)
    HHPredAssistant(alignmentBrowser, aa)
    blast_assistant(alignmentBrowser)


    return alignmentBrowser

def letsRock(geneLinkList,phagePage_URL):
    genemarkAssistant(phagePage_URL)
    counter =1
    for geneURL in geneLinkList[::-1]:
        #format_thing=()
        print('#######################################################\n                     GENE ',counter,
                '\n########################################################')
        try:
            try:
                browser.quit()
            except:
                ''
            try:
                alignmentBrowser.quit
            except:
                ''
        except:
            ''
        counter +=1
        alignmentBrowser = functionCaller(geneURL)
        input('Press ENTER to continue to next gene')



#letsRock(geneLinkList,phagePage_URL)

def letsrock2(geneLinkList,phagePage_URL):
    genemarkAssistant(phagePage_URL)
    counter = 1
    genedict = {}
    for geneURL in geneLinkList[::-1]:
        genedict[counter]= geneURL
        counter +=1
    browser.quit()
    # keeps user in loop to go through gene list
    def control_loop():
        key = ''
        while key == '':
            try:

                # halt exception to stop code and retry
                class HaltException(Exception): pass

                choice = input('\nPlease enter the number of the gene whose information you want to call.\n'
                               'You can also press ENTER to call a batch of the next 5 genes.\nType \'exit\' to quit.'
                               '\nUSER INPUT: ')

                if choice == '':
                    choice = oldchoice + 1
                    try:
                        functionCaller(genedict[choice])
                    except:
                        ''
                    try:
                        functionCaller(genedict[choice+1])
                    except:
                        ''
                    try:
                        functionCaller(genedict[choice+2])
                    except:
                        ''
                    try:
                        functionCaller(genedict[choice+3])
                    except:
                        ''
                    try:
                        functionCaller(genedict[choice+4])
                    except:
                        ''
                    try:
                        functionCaller(genedict[choice+5])
                        oldchoice = choice + 5
                    except:
                        ''
                elif choice == 'exit':
                    quit()

                elif choice == 'refresh':
                    raise HaltException
                    continue

                else:
                    choice = int(choice)
                    functionCaller(genedict[choice])
                    oldchoice = choice



                # elif choice == '?':
                #     print('type a gene number to call its')

            except Exception as e:
                print('Make sure you are entering a value corresponding to a gene number.')
                input('Press ENTER to continue.')
                continue
    control_loop()


letsrock2(geneLinkList,phagePage_URL)