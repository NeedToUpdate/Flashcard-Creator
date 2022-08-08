# Flashcard Creator

This is a small and easy python script for creating flashcards for ESL classes. It takes a folder of images, and creates a pdf file of images with the words in large font on the back.

# Example Usage

The words I want to use are car, farm, target, arm. The target letters are 'ar'.

1. make a folder named 'ar words' in the Create Flashcards Here folder.
2. add some images, making sure their names are the key words. e.g. arm.png, target.jpg
3. run create_flashcards.py

```
    What is the folder name?
    >ar words
```

the name of the folder

```
    Who is the author?
    >
```

you can leave it blank, or write your name

```
    Highlight the first letter? (yes/no/input)
    >input
```

'yes' will make the first letter green  
'no' will make it all black  
'input' allows you to choose a custom letter combo

```
    What should be highlighted?
    >ar
```

in this example, 'ar' in c**ar**, **ar**m, t**ar**get will be highlighted green.

press enter, and see your flashcards!

# How To Install

This is intended to be shared with ESL teachers who are not tech oriented, so python installation files were included in the folder to make it easier to install.

## Windows

1. Go to /Install Python/
2. Double click 'python windows.exe'. Install it.
3. Double click 'RUN AFTER INSTALL WINDOWS.bat'
4. Double click the create_flashcards.py file in the 'Create Flashcards Here' folder to make flashcards!

## Mac

1. Go to /Install Python/
2. Double click 'python mac.pkg'. Install it.
3. Open 'Terminal'
4. type this:  
   `pip3 install reportlab Pillow`
5. press enter
6. Double click the create_flashcards.py file in the Create Flashcards Here folder. It will open Idle
7. Click 'run' or F5
