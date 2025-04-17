from lxml import etree
import sys
import re

def aiken_to_moodle(aiken_file_path, moodle_file_path, tag=""):
    with open(aiken_file_path, 'r') as file:
        aiken_questions = file.read()

    quiz = etree.Element('quiz')
    questions = aiken_questions.strip().split('\n\n')
    
    for question in questions:
        lines = question.split('\n')
        prefix = ""
        if tag != "":
            prefix = "[#"+ tag +"] " 
        if bool(re.match(r'^\d+\. ', lines[0])):
            question_text_real = prefix + lines[0].split('. ', 1)[1]
        else:
            question_text_real = prefix + lines[0]
        answers = lines[1:5]
        
        correct_answer = lines[5].split(': ')[1]
        correct_index = ord(correct_answer) - ord('A')
        
        question_element = etree.SubElement(quiz, 'question', type='multichoice')
        name = etree.SubElement(question_element, 'name')
        etree.SubElement(name, 'text').text = question_text_real[:30] + "..."
        
        questiontext = etree.SubElement(question_element, 'questiontext', format="html")
        question_text = etree.SubElement(questiontext, "text")
        question_text.text = etree.CDATA('<p>' + question_text_real + '</p>')

        default_grade=etree.SubElement(question_element,"defaultgrade")
        default_grade.text = "0.33333"
        if tag !="":
            tags = etree.SubElement(question_element,'tags')
            tag_element = etree.SubElement(tags,"tag")
            etree.SubElement(tag_element,"text").text = "#"+tag
        
        shuffle = etree.SubElement(question_element,"shuffleanswers")
        shuffle.text = '1'

        radio = etree.SubElement(question_element,'single')
        radio.text='true'
        
        answernumbering = etree.SubElement(question_element, 'answernumbering')
        answernumbering.text = 'abc'

        for idx, answer in enumerate(answers):
            answer_text = answer[3:]  # Extract the answer text without the prefix (e.g., "A) ")
            
            # Determine if the current answer is the correct one
            fraction = '100' if idx == correct_index else '0'
            
            answer_element = etree.SubElement(question_element, 'answer', fraction=fraction, format="moodle_auto_format")
            etree.SubElement(answer_element, 'text').text = etree.CDATA(answer_text)

    # Pretty print and write to file
    document = etree.ElementTree(quiz)
    document.write(moodle_file_path, pretty_print=True, xml_declaration=True, encoding='utf-8')

aiken_file_path = sys.argv[1] 
moodle_file_path = sys.argv[2]
# Default situation when no tag
tag=""
if len(sys.argv)>=4:  
    # EXAM only works properly on bulk import with lower case tags for some reason
    tag = str(sys.argv[3]).lower()


aiken_to_moodle(aiken_file_path, moodle_file_path,tag)
