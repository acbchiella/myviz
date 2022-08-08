# Virtual Environment

1 - create a virtual environment
`python3 -m venv venv`

2 - activate the environment
`source ./venv/bin/activate`

3 - Upgrade
`python3 -m pip install --upgrade pip setuptools wheel`

# Dependencies
- VPython: `python3 -m pip install -U vpython`

- wxPython (It is not working, change to QT): `python3 -m pip install -U -f https://extras.wxpython.org/wxPython4/extras/linux/gtk3/ubuntu-18.04 wxPython`

- QT: `python3 -m pip install PyQt5`
- QTWEB: `python3 -m pip install PyQtWebEngine`


# Before change:
In `/venv/lib/python3.6/site-packages/vpython/no_notebook.py`, changes `os.system('python ' + filename + ' http://localhost:{}'.format(port))` by `os.system('python ' + f'{sys.path[0]}/vpy/main_gui.py' + ' http://localhost:{}'.format(port))`.

# Example
![image](https://user-images.githubusercontent.com/44218268/183320204-872574cd-05f3-4574-8793-b615422804e0.png)

