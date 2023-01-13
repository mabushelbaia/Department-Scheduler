# Department Courses Scheduler

🔗 | [Project Description](Project1_Description.pdf)  
🔗 | [Report](Report.pdf)

an implementation of the genetic algorithm use to search for an optimized/optimal schedule.

To run this program you should have python3 and git installed
First clone this directory by running
```bash
git clone https://github.com/mabushelbaia/Department-Scheduler.git
cd Department-Scheduler
```
or just download the code from the website.
install required python librariers
```bash
pip install -r requirements.txt
```
Running ```main.py``` will give you an output on the console regarding the schedule attributes as shown below.
![[assests/Pasted image 20230113131028.png]]

and it would genereate 2 files under ./templates the first one is ```index.html``` and ```
schedule.txt``` the first is an html page and will be used as a gui, and the latter is just saving the list of courses in-case its needed.

# Demo

## Extreme Minimizing One aspect
Going to an extreme route not giving regard to any other aspect rather than optimizing one aspect
is going to fail the schedule, e.g., extremely optimizing to have minimum number of days on Saturday.

![two](https://user-images.githubusercontent.com/47891125/212328481-2dbd7f06-998d-4964-8815-b298fa93467c.png)


As we notice the conclicts are going up, which is not good for our schedule, and if we check the [Schedule](templates/extreme_sat.html) we see that the slots are not distributed correctly, for example, digital systems is offered 5 times on (T, R ) out of 8.

## Resonable Minimizing
As shown earilir optimizing one aspect is a poor aproach so we are going to run an optimized way with giving resonable weight for each penalty.
![test](https://user-images.githubusercontent.com/47891125/212328849-eb3560c7-f6fb-40e6-a26d-3a7847a0832f.png)
As we can see in the picture above we cut the Saturday slots almost by half, reduce the conflicts to almost minimum; minimum is 33 as stated on the report, we minimized the late by half, we can rather minimize the any attribute by increasing its penalty. And as we can see in the [Schedule](templates/optimized.html) our course are fairly distributed. 