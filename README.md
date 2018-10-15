# TensorRT-googlenet-opencv
use opencv to read .jpg and accelerate using tensorrt

Testing on TX2,CUDA9.0,OPENCV3.3.1,TENSORRT4.0

Usage:

1.mkdir image && mkdir model
and put images for testing and caffemodel and deploy.prototxt in folder "image" and "model" separately

2.modify Makefile to fit your environment

3.try to list your testing images in file "test"(this is not a txt!)

4.modify related path and input,output,classes names,image mean (in BGR order) in main.cpp according to your model 

5.make all 

6.you will find an executable file called "googlenet",try
./googlenet


