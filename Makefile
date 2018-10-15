######################################
#
######################################
#source file
#源文件，自动找所有.c和.cpp文件，并将目标定义为同名.o文件
SOURCE	:=	$(wildcard ./*.c) $(wildcard ./*.cpp)
OBJS	:=	$(patsubst %.c,%.o,$(patsubst %.cpp,%.o,$(SOURCE)))

#target you can change test to what you want
#目标文件名，输入任意你想要的执行文件名
TARGET  := googlenet

#compile and lib parameter
#编译参数
CC      := g++
LIBS    := 
LIBS    += -L"/usr/local/cuda-9.0/targets/x86_64-linux/lib" 
LIBS    += -L"/usr/local/lib"
LIBS    += -L"/usr/local/cuda-9.0/lib"
LIBS    += -L"/usr/local/cuda-9.0/lib64" 
LIBS    += -lnvinfer -lnvparsers -lnvinfer_plugin -lcudnn -lcublas -lcudart_static -lnvToolsExt -lcudart -lrt -ldl -lpthread

LDFLAGS :=
DEFINES :=  
INCLUDE := -I./ 
INCLUDE += -I/usr/local/cuda-9.0/targets/aarch64-linux/include/ 
CFLAGS  := -std=c++11 -g -Wall -O3 $(DEFINES) $(INCLUDE)

PKGS:= opencv
CFLAGS+=$(shell pkg-config --cflags $(PKGS))
LIBS+=$(shell pkg-config --libs $(PKGS))

CXXFLAGS:= $(CFLAGS) 
#i think you should do anything here
#下面的基本上不需要做任何改动了
.PHONY : objs clean rebuild

all : $(TARGET)

objs : $(OBJS)

rebuild: clean all
   
clean :
	rm -fr ./*.o
	rm -fr $(TARGET)

$(TARGET) : $(OBJS)
	$(CC) $(CXXFLAGS) -o $@ $(OBJS) $(LDFLAGS) $(LIBS) 
