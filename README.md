# Generative-Art

I have only tested this on Ubuntu 20.04.

A selection of generative art scripts written in Python with the intention of using my AxiDraw to plot them onto paper.

This project has evolved into a small python package which has functions and classes, which I reuse in other scripts and saves me writing the same code over and over again. It also includes basic tool for generating scripts and doing basic tasks that I do on a regular basis.
  
This is really built for my own personal use and is a constantly evolving project, but I thought people may enjoy / be interested in it, so that is why I am making it public.

You can get these scripts without the python module integration by cloning the 0.1.1 tag, go here: https://github.com/JakobGlock/Generative-Art/tree/0.1.1


### Setup

These scripts have been made using Python 3.8.2

Install some dependencies, on Linux this very simple you just run the following command in a terminal window:

`sudo apt install python-cairo libcairo2-dev`

Create a Python virtual environment and activate it:

```
cd /to/the/repo/directory/on/your/computer/Generative-art
python3 -m venv venv
source venv/bin/activate
```

You will also need to install some packages for Python which can be done using the following command:

`pip3 install -r requirements.txt`


### Running Scripts

You can use the generate tool to run the scripts, to get more information run the following command:

`./generate --help`


To generate an artwork:

`./generate artwork new Line_Grid.py`

To generate the same artwork, but 10 of them and in SVG format:

`./generate artwork new Line_Grid.py -n 10 --svg`

This will save 10 files in SVG format into the `Images/Line_Grid` folder, see `./generate --help` for more options and information.


To create a new script/project, run the following command:

`./generate project new my_cool_script.py`

This will create a basic script from a template file to get you started.
 

### Sample Images

#### Circular
![Circular](/Images/Circular/0bde255-sample.png)

#### Line_Grid
![Line_Grid](/Images/Line_Grid/c314c507-sample.png)

#### Line_Walker
![Line_Walker](/Images/Line_Walker/857172e8-sample.png)

#### Magnetic_Flow
![Magnetic_Flow](/Images/Magnetic_Flow/9d6a69dd-sample.png)

#### Mosaic_Circles
![Mosaic_Circles](/Images/Mosaic_Circles/1e299f47-sample.png)

#### Parallel_Lines
![Parallel_Lines](/Images/Parallel_Lines/a5c334c2-sample.png)

#### Vertical_Lines
![Vertical_Lines](/Images/Vertical_Lines/125c3d4d-sample.png)
