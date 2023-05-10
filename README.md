# Automarkup
Automarkup dataset with images face

Important! this software is designed for Linux kernel operating systems

To use this algorithm:
You need to configure the environment and install dependencies:

1) sudo apt-get install build-essential cmake pkg-configsudo 
   sudo apt-get install libx11-dev libatlas-base-dev 
   sudo apt-get install libgtk-3-dev libboost-python-dev
  
2) sudo apt-get install python-dev python-pip python3-dev python3-pip
   sudo -H pip2 install -U pip numpy
   sudo -H pip3 install -U pip numpy

3) sudo pip2 install virtualenv virtualenvwrapper
   sudo pip2 install virtualenv virtualenvwrapper
   echo “# Virtual Environment Wrapper” >> ~/ .bashrc
   echo “source /usr/local/bin/virtualenvwrapper.sh” >> ~/ .bashrc
   source ~/.bashrc

4) mkvirtualenv env-p python3
   workon env
   pip install numpy scipy matplotlib scikit-image scikit-learn ipython
   deactivate
   
5) wget http://dlib.net/files/dlib-19.6.tar.bz2
   tar xvf dlib-19.6.tar.bz2
   cd dlib-19.6/
   mkdir build
   cd build
   cmake ..
   cmake –build . –config Release
   sudo make install
   sudo ldconfig
   cd ..

6) pkg-config –libs –cflags dlib-1

7) cd dlib-19.6
   python setup.py install
   rm -rf dist
   rm -rf tools/python/build
   rm python_examples/dlib.so
   
8) pip install insightface face_recognition onnxruntime onnxruntime-gpu
   pip install pandas numpy scipy sklearn sklearn-image Tk 
   
All the necessary libraries in the file requirements.txt

Accepted use!





   
