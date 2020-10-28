from bs4 import BeautifulSoup 
import requests
import string

URL = 'https://www.who.int/emergencies/diseases/novel-coronavirus-2019/question-and-answers-hub/q-a-detail/coronavirus-disease-covid-19' 


def sort_info():
    """
    Function that web scraping the data from the BeautifulSoup object
    Args:
        Nothing
    Return:
        returns a tuple of questions, answers and the last update of the web page
    """
    soup = make_soup()

    info = soup.find(id='sf-accordion')
    unordered_data = str(info.encode('utf-8')).split('div class="sf-accordion__panel">')[1::]

    temp = []
    questions = []
    answers = []

    # Splites the data to more useabel question & answer block    
    data_to_qa_block = '\\n<div class="sf-accordion__trigger-panel">\\n<a class="sf-accordion__link" href="#">'
    
    # Splites the data to list : first place question, sec place answer
    unordered_que_and_ans = '/div>\\n<div class="sf-accordion__content">\\n<p class="sf-accordion__summary">\\n<p>'
    
    for first_element in unordered_data:
        temp = first_element.split(data_to_qa_block)[1]
        temp = temp.split(unordered_que_and_ans)
        questions.append(temp[0])
        answers.append(temp[1])


    questions = get_questions(questions)
    answers = get_answers(answers)
    last_update = get_last_update(soup)

    print("Finished getting all the questions and answers")
    return questions, answers, last_update

def make_soup() -> BeautifulSoup:
    """
    Function that gets the html page
    Args:
        Nothing
    Return:
        returns a BeautifulSoup object.
    """
    request = requests.get(URL, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(request.text, features = 'html.parser')
    return soup


def get_questions(questions : list) -> list:
    """
    Function that 'cleans' the answers from html tags.
    Args:
        answers (list) : The answers variable we need to 'clean'.
    Return:
        returns an answes list after cleaning it.
    """

    final_questions = []
    for question in questions:
        q = question.split('\\r\\n                            ')[1][4::]
        final_questions.append(q)
    
    return final_questions


def get_answers(answers : list) -> list:
    """
    Function that 'cleans' the answers from html tags.
    Args:
        answers (list) : The answers variable we need to 'clean'.
    Return:
        returns an answes list after cleaning it.
    """

    last_element_block = '</p>\\n</p>\\n</div>\\n</div>\\n<!-- end:sf accordion panel -->\\n</div>'
    answers[len(answers) - 1] = answers[len(answers) - 1].split(last_element_block)[0]

    unordered_data = '</p>\\n</p>\\n</div>\\n</div>\\n<!-- end:sf accordion panel -->\\n<!-- sf accordion panel -->\\n<'
    final_answers = []
    
    for ans in answers:
        temp = ans.split(unordered_data)[0]
        
        if '</p><ul><li>' in temp:
            temp = temp.replace('</p><ul><li>', ',')

        if '</li><li>' in temp:
            temp = temp.replace('</li><li>', ' ')

        if '</li></ul><p>' in temp:
            temp = temp.replace('</li></ul><p>', '\\n')
        
        if '</p><p>' in temp:
            temp = temp.replace('</p><p>', '\\n')
        
        if '<strong>' in temp or '</strong>' in temp:
            temp = temp.replace('<strong>',  ' ')
            temp = temp.replace('</strong>', ' ')
        
        while '<em>' in temp:
            first = temp.index('<em>')
            last = temp.index('</em>') + 5
            d = temp[first : last]
            temp = temp.replace(d, ' ')
        
        while '<a href=' in temp:
            first = temp.index('<a href=')
            last = temp.index('>') + 1
            d = temp[first : last]
            temp = temp.replace(d, '')
            temp = temp.replace('</a>', ' ')
            
        if '\\n' in temp:
            temp = temp.replace('\\n', '\n')

        if '\\t' in temp:
            temp = temp.replace('\\t', ' ')
        
        printable = set(string.printable)
        filter(lambda x: x in printable, temp)

        final_answers.append(temp)
    
    return final_answers

def get_last_update(soup : BeautifulSoup) -> str:
    """
    Function that web scraping the last update title from the web page
    Args:
        soup (BeautifulSoup) : The web page were scraping from
    Return:
        returns a string of the laste update title
    """

    last_update_block = soup.find('p', 'qa-details__summary')
    last_update = last_update_block.text
    last_update = last_update[16:19] + 'of ' + last_update[19::]
    
    return last_update