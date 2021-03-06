## Program Progress Form Updater for Biological Engineering Major

### How to run the PPF Auto-Updater
#### Directory Setup
In order to make sure the program will run properly, ensure the following files are located in the primary directory (`ppfproj` or `ppfproj-master`)
- `masterfile.py` - this is the main file that runs the PPF updater
- `blankPPF.xlsx` - the updater will fill in a copy of this for each student, so make sure it is formatted as desired
- `Transcript` - this folder, which will be empty on github for confidentiality, is where you will put the transcript file, called `transcript.xlsx`, as a spreadsheet (see formatting instructions below)
- `Students` - this folder, also empty on github, will be where the student PPFs as well as the summary file `summary.txt` appear
- `support_files` - this folder will contain several support files that help the program run... most are code, but the following are important:
    - `advanced_bio.xlsx` - a list of courses that satisfy upper-level biology, in no particular order
    - `engri_courses.xlsx` - a list of courses that satisfy the ENGRI (intro engineering) requirement
    - `other_yes.xlsx` - a list of courses not on the engineering website but that have been approved to satisfy liberal arts requirements for the College of Engineering
    - `research_ta_etc.xlsx` - a list of courses like research and TA credit from which you can get up to 4 credits of focus area credits, and from there 
    
##### What's in the files?
- `transcript.xlsx` should have the following columns, with column names written *exactly* as shown below in bold.  The program can handle multiple sheets of transcripts in a single excel file, or all transcripts on a single sheet, it doesn't matter.  Column names:
    - **Effdt Preferred Name** (student name in the format *last,first middle* ie *Popp,Joshua Michael*)
    - **Netid** (student net ID)
    - **Employee Id** (student ID)
    - **Expected Grad Term Ldescr** (expected graduation, can also use **Sdescr**)
    - **Academic Term Ldescr** (term in which the course was taken, can also use **Sdescr**)
    - **Class Descr** (course description, in words, ie Intro to Economics)
    - **Subject** (department under which the course is listed, ie BEE)
    - **Catalog Nbr** (course number, ie 3600)
    - **Official Grade** (letter grade received for the course)
    - **Unt Taken** (number of credits the course was taken for)
    - **Advisor** (advisor name, again in the format *last,first m*)
    - **AP Test Component Ldescr** (name of the AP course, from a specific list)
    - **AP Test Sdescr** (if the course was an AP course, will say 'AP', else empty cell)
    - **Score** (score received on AP exam for AP course)
    - **TR School Descr** 
    - **TR School Subject**
    - **TR School Crse Nbr**

#### How to run
Download this directory from Github with help from the bright green `Clone or Download` button in the upper right.  

Once the directory is set up as above, all you need to do is run `masterfile.py` and you should find the `Students` folder populated with a summary file `summary.txt`, as well as students PPFs sorted into folders by graduation date.  

For more detailed instructions on how to run, go to this [link](https://docs.google.com/document/d/1Kkpzor1BxUQBxaVvzJz5Bn-kCEVqtxRTXGclJUnE4t8/edit?usp=sharing).

### What does it do?
1.  The first thing 

### What doesn't it do?
- Foreign language requirements
- Transfer requirements
- Fix existing problems in PPFs 

### Other Implementation Details
#### AP Course Descriptions
List of acceptable course descriptions for AP Courses (if the course is not listed with one of these exact descriptors, credit will not be given by the program):
- Biology
- Chemistry
- Computer Science A
- Mathematics: Calculus BC
- Physics C - Mechanics
- English Language &Composition
- English Literature &Compostn
- Spanish Language
- Spanish Literature
- French Language
- French Literature
- German Language & Culture
- Italian Language & Culture
- Economics: Macroeconomics
- Economics: Microeconomics
- Psychology
