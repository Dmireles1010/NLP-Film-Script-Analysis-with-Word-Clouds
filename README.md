# Film Word Cloud

Film Word Cloud is a project that visualizes the frequency of words spoken by characters in a film. The size of each word in the word cloud represents its occurrence frequency. Using Natural Language Processing (NLP) techniques, the project removes stopwords and identifies commonly spoken words by specific characters. It leverages film transcripts as the data source to determine the sentences spoken by the characters, which are then used to create a word count dictionary. The word cloud is displayed using Tkinter, a Python library for creating graphical user interfaces.

## Instructions

1. Install the NLTK library by running the following command:
`pip install nltk`
2. Run the project using the following command:
`python wordcloud.py`
3. When prompted, enter the name of the text file containing the film transcript you want to visualize as a word cloud. The text files should be located in the "FilmScripts" folder.
Example: If the transcript file is named "Bee Movie.txt", enter `Bee Movie`.

The project will generate a graphical word cloud using Tkinter, representing the frequency of words spoken by characters in the specified film transcript. You can select different characters from the film on the right side of the graphical interface to view word clouds specific to each character.

Before running the project, make sure you have installed the necessary dependencies, including the NLTK library, and ensure that the film transcript files are available in the designated "FilmScripts" folder.

# Preview
![Preview](https://i.imgur.com/MvFYkih.png)

## License

This project is licensed under the [MIT License](https://github.com/Dmireles1010/NLP-Film-Script-Analysis-with-Word-Clouds/blob/master/License.txt).


