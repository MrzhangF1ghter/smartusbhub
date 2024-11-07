# SmartUSBHub
Control your usb devices connect or disconnect to the host using simple command.   
For more details, please read project's [wiki page](https://github.com/MrzhangF1ghter/smartusbhub/wiki)

## How to use

1. Clone this repository to your computer

   - For Windows10 users:

     ```shell
     git clone -b windows_patch https://github.com/MrzhangF1ghter/smartusbhub.git
     ```

     or download release [here](https://github.com/MrzhangF1ghter/smartusbhub/releases/tag/V1.0_windows)

   - For other OS version users:

     ```shell
     git clone https://github.com/MrzhangF1ghter/smartusbhub.git
     ```

     or download release [here](https://github.com/MrzhangF1ghter/smartusbhub/releases/tag/V1.0)

2. Install python3 environment [here](https://www.python.org/downloads/)

3. Setup python virtual environment

   ```shell
   cd ./smartusbhub
   python -m venv venv
   ```

4. Enter virtual environments

   - For Windows users:

     ```bat
     .\venv\Scripts\activate.bat
     ```

   - For Linux and MacOS users:

     ```shell
     source ./venv/bin/activate
     ```

   - Install `pyserial` library (Windows users skip this step)

     ```shell
     pip install pyserial
     ```

5. Connect your smartusbhub comunication port (left-side) to your computer

6. Look up device comunication port name:

   - for windows users:  `COMx`
   - For linux users: `/dev/ttyACMx`
   - For macOS users: `/dev/cu.usbmodemx`

7. Run test.py for fun! 

   ```bat
    python .\test.py -p COM3
   ```


## Integrate to your project

You can intergrate in your project by importing smartusbhub library.

