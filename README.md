## Description

An autonomous Nerf sentry gun. Computer vision is driven by Python and OpenCV on a Raspberry Pi. Ultimately, this repository will include a parts list, any CAD files, and instructions on how to put together your own. For now, I will just going one step at a time.

Also, I hate instructions that assume you know a lot, so I will be as thorough as I can without being pedantic, and provide resources where needed.

## Resources
Below are many links that I found very helpful. This is not the first sentry project, so I am just looking to improve as much as I can on what has been accomplished. Anyway, credit where credit is due:
- http://www.instructables.com/id/Nerf-Vulcan-Sentry-Gun/
- http://www.instructables.com/id/Autonomous-Sentry-Turret/
- http://www.instructables.com/id/Autonomous-Paintball-Sentry-Gun/

## Installation
In your terminal, navigate to wherever you want to download everything and run
```bash
git clone https://github.com/chendrix4/sentry
```
This will create a folder **sentry** in your current directory and store everything in there. If you are on Windows, simply download the zip from the top right (see the green **clone or download** button).

### Virtual Environments
If you are using Linux, you will want to set up a virtual environment. Quick explanation is that many Linux applications employ Python. You do not want to mess with those applications, so all you are doing is creating another Python environment to work with.
To create this environment, do the following:
```bash
sudo apt-get install python3-venv
python3  -m venv sentry
```
Once installed, a **bin** directory will appear in you simply activate the virtual environment by running
```bash
source bin/activate
```
and exit at any time by running
```bash
deactivate
```
Make **SURE** to activate your virtual environment when you start editing.

### Theory of Operation
OpenCV is a very powerful and robust computer vision library. The script runs with a combination of recognition and tracking. Once a target is acquired, the computer continues to track all movement. A detection scan continues to run every n*th* frame. If nothing is detected for 5 passes in a row, and tracking is currently failing, the program recognizes that there is no target in frame. This model allows for the accuracy of detection combined with the speed of tracking, without sacrificing anything.

The program can be run with several tracking algorithms. I have found that KCF works best (reports tracking failure most quickly and most impervious to false positives). Currently, there are many constants used that need finer tweaking. However, some simple tests show the overall operation to be working.
