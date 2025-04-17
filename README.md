# Docs
Docs, Scripts, Code, etc

## Aiken to MoodleXML

The file aiken_to_moodleXML.py converts multiple choice questions with only one correct answer and four choices from Aiken format to a valid MoodleXML file.

### Use

Clone the repository, and prepare your questions into a text file. Run the file using: 

```
python aiken_to_moodleXML.py <path/to/aiken_questions.txt> <path/to/new_file.xml> <tag>
```

In the path to new file, the filename you enter is the one created at the path entered.

The tag argument adds in a tag element, you may also leave this empty.

