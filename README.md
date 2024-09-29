# ReWLis


# Audio player for

- Implementation of the RWL concept. "Read While You Listen"
- Synchronous reading of two books: Russian or English
- Synchronous listening of two books: Russian or English
- Online catalog of audiobooks included

# Catalog of books:

- Dickens_Charles_-_A_Christmas_Carol
- Kafka Franz The Metamorphosis
- Kuttner Henry The Ego Machine
- Lewis Carroll Alices Adventures in Wonderland
- Wells Herbert The Time Machine

# Binary and source download

- Last release for Android 
- Last release for Windows x64 

# Install and run from sources (on Windows)

- Download sources
- Install python 3.9 - tested only this version
- Create virtual env, run command "python.exe -m venv venv"
- Activate venv, run command "venv/Scripts/activate.bat"
- Upgrade pip, run command "python.exe -m pip install -upgrade pip"
- Install requirements, run command "pip install -r requirements.txt"
- Run main.py with python

# For own build apk (for run this file on Android) 

- Install Ubuntu 22 on VirtualBox
- Run virtual machine with Ubuntu 22
- Install depends: https://python-for-android.readthedocs.io/en/latest/quickstart/ for Ubuntu 22
- Clone git in you project on github
- Copy git in you project on local machine (on Windows)
- Install python 3.9 - tested only this version
- Create virtual env, run command "python.exe -m venv venv"
- Activate venv, run command "venv/Scripts/activate.bat"
- Upgrade pip, run command "python.exe -m pip install -upgrade pip"
- Install requirements, run command "pip install -r requirements.txt"
- run commands in terminal Ubuntu:
   - $ wget --quiet --output-document=setup.sh https://.../setup.sh
   - $ chmod +x setup.sh 
   - $ ./setup.sh
- Waiting while run daemon.sh, no close terminal
- Commit and push new version in you config.sh on GitHub
- Create file ftpconfig.py with vars HOST, USER, PASSWORD for access to ftp server for uploading exe files
- Run local (on Windows) build.py for create exe files and upload on server with change version in latest/latest.txt
- Wait all complete
- Run .apk with arch 'armeabi-v7a' on Android; 
- Arch 'x86_64' may be run in emulator on Android Studio

# About RWL-concept

Listen or read? The answer is to read while listening!

There has been a heated debate about language learning for years. So, the big question is: should we learn new languages by reading? Or is audio the most effective method? Some argue that text is definitely the way forward.

“Hey, but I heard audio is just as effective,” someone always chimes in. It’s just not set in stone, and many believe that neither side will ever have a definitive say on the matter.

Fortunately, research over the past decades has led language experts to an incredible conclusion: it’s not about choosing one or the other. It’s about using the best of both worlds to achieve the results you want, and giving students the opportunity to continually improve on one method by using its counterpart.

They called it Reading While Listening (RWL), and it truly is the future of learning a new language. RWL as a language learning method has been widely studied, and its amazing benefits have not only given experts food for thought, but also provided students with the opportunity to improve both aspects of their learning (listening and reading) at the same time. With less effort.

Among them:

#### 1. Focus

Reading while listening has been shown to increase concentration on the text (by forcing learners to eliminate background noise and focus on the sound they are listening to) and is seen as a great alternative for young children and adults with limited attention spans.

#### 2. Improving Pronunciation

It’s one thing to read a word, and another to pronounce it. After all, is colonel pronounced the way it’s read? What about chorus or queue? All those tricky words that we can repeat incorrectly over and over again before we even hear someone else pronounce them. RWL ensures that we know how to pronounce a word as soon as we read it. Pretty cool, huh?

#### 3. Increased Motivation

The above-mentioned studies conducted in the past decades have definitely shed a positive light on this method of language learning. Children in Taiwan were subjected to a 26-week study in which two groups were taught English using different methods, one with RWL and one without (Chang, C.S. (2011). The effect of reading while listening to audiobooks: Listening fluency and vocabulary growth (Asian Journal of English Language Teaching, 21, 43–64). The results spoke for themselves: the RWL group significantly outperformed their non-RWL counterparts, and their motivation to study for future lessons increased more than the other group.

#### 4. Improving Fluency

According to Dictionary.com, fluency is “the ability to speak or write a particular foreign language with ease.” This trait determines how well you can string words together into phrases and sentences, rather than how you pronounce them. It is what allows you to communicate with native speakers at all. The aforementioned study conducted in Taiwan concluded that RWL helps learners speak better than just reading because the voice of the narrator will remain in our memory and come back to us whenever we need it.

#### 5. Closer to Native Speaker Skills

Last but not least, it is important to note that using reading and listening at the same time can give you a better understanding of how native speakers speak and think, which is something that only one of the two methods will not do. Reading and listening will teach you to absorb a new language like a native, and you will begin to improve your language skills like never before.

In conclusion, reading while listening is a new and effective method for learning a new language, and the most innovative teachers and companies are already using it to teach their students. The future is already in RWL!