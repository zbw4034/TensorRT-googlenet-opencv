#include <assert.h>
#include <fstream>
#include <sstream>
#include <iostream>
#include <cmath>
#include <algorithm>
#include <sys/stat.h>
#include <cmath>
#include <time.h>
#include <string>
#include <cuda_runtime_api.h>


#include <memory>
#include <fstream>
#include <tuple>



#include <opencv2/imgproc.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/dnn.hpp>

#include "NvInfer.h"
#include "NvCaffeParser.h"
#include "common.h"

static Logger gLogger;
using namespace nvinfer1;
using namespace nvcaffeparser1;



// stuff we know about the network and the caffe input/output blobs
static const int INPUT_H = 224;
static const int INPUT_W = 224;
static const int IMAGE_CHANNEL = 3;
static const int OUTPUT_SIZE = 2;
static const int BATCH_SIZE = 1;

const char* INPUT_BLOB_NAME = "data";
const char* OUTPUT_BLOB_NAME = "prob";

const std::string model{"model/deploy.prototxt"};
const std::string weights{"model/googlenet_iter_4180.caffemodel"};
const std::string planFilePath{"model/googlenet.engine"};
std::vector< std::string > outputs{ OUTPUT_BLOB_NAME };
const std::string list_file{"test"};

const int LINE_LENGTH = 255;
char image_name[LINE_LENGTH];


void creatGIEEngine(const std::string& deployFile, // name for caffe prototxt
                    const std::string& modelFile,
                    const std::string& planFilePath)
{
    // parse the caffe model to populate the network, then set the outputs
    std::cout << "Reading Caffe prototxt: " << deployFile << "\n";
    std::cout << "Reading Caffe model: " << modelFile << "\n";

    IBuilder* builder = createInferBuilder(gLogger);
    INetworkDefinition* network = builder->createNetwork();
    ICaffeParser* parser = createCaffeParser();

    bool useFp16 = builder->platformHasFastFp16();

    DataType modelDataType = useFp16 ? DataType::kHALF : DataType::kFLOAT; // create a 16-bit model if it's natively supported
    const IBlobNameToTensor *blobNameToTensor =
        parser->parse(deployFile.c_str(), // caffe deploy file
                      modelFile.c_str(), // caffe model file
                      *network, // network definition that the parser will populate
                      modelDataType);

    assert(blobNameToTensor != nullptr);
    // the caffe file has no notion of outputs, so we need to manually say which tensors the engine should generate
    for(auto& s : outputs)
        network->markOutput(*blobNameToTensor->find(s.c_str()));

    // Build the engine
    builder->setMaxBatchSize(BATCH_SIZE);
    builder->setMaxWorkspaceSize(16 << 20);

    // set up the network for paired-fp16 format if available
    if(useFp16)
        builder->setHalf2Mode(true);

    ICudaEngine* engine = builder->buildCudaEngine(*network);
    assert(engine);


    nvinfer1::IHostMemory* modelStream = engine->serialize();
    assert(modelStream != nullptr);

    std::stringstream gieModelStream;
    gieModelStream.seekg(0, gieModelStream.beg);
    gieModelStream.write(static_cast<const char*>(modelStream->data()), modelStream->size());
    std::ofstream outFile;
    outFile.open(planFilePath);
    outFile << gieModelStream.rdbuf();
    outFile.close();

    network->destroy();
    parser->destroy();
    engine->destroy();
    builder->destroy();
    shutdownProtobufLibrary();
}

nvinfer1::ICudaEngine* loadGIEEngine(const std::string planFilePath)
{
    // reading the model in memory
    std::cout << "Loading TRT Engine..." << std::endl;
    assert(fileExists(planFilePath));
    std::stringstream gieModelStream;
    gieModelStream.seekg(0, gieModelStream.beg);
    std::ifstream cache(planFilePath);
    assert(cache.good());
    gieModelStream << cache.rdbuf();
    cache.close();

    // calculating model size
    gieModelStream.seekg(0, std::ios::end);
    const int modelSize = gieModelStream.tellg();
    gieModelStream.seekg(0, std::ios::beg);
    void* modelMem = malloc(modelSize);
    gieModelStream.read((char*) modelMem, modelSize);

    nvinfer1::IRuntime* runtime = nvinfer1::createInferRuntime(gLogger);
    nvinfer1::ICudaEngine* engine = runtime->deserializeCudaEngine(modelMem, modelSize, nullptr);
    free(modelMem);
    runtime->destroy();
    std::cout << "Loading Complete!" << std::endl;
    return engine;
}

void timeInference(IExecutionContext& context, unsigned char * input, float* output,  int batchSize)
{
    const ICudaEngine& engine = context.getEngine();
    // input and output buffer pointers that we pass to the engine - the engine requires exactly ICudaEngine::getNbBindings(),
    // of these, but in this case we know that there is exactly one input and one output.
    assert(engine.getNbBindings() == 2);
    void* buffers[2];

    // In order to bind the buffers, we need to know the names of the input and output tensors.
    // note that indices are guaranteed to be less than ICudaEngine::getNbBindings()
    int inputIndex = engine.getBindingIndex(INPUT_BLOB_NAME);
    int outputIndex = engine.getBindingIndex(OUTPUT_BLOB_NAME);

    // allocate GPU buffers
    DimsCHW inputDims = static_cast < DimsCHW && >(engine.getBindingDimensions(inputIndex));
    DimsCHW outputDims = static_cast < DimsCHW && >(engine.getBindingDimensions(outputIndex));
    size_t inputSize = batchSize * inputDims.c() * inputDims.h() * inputDims.w() * sizeof(float);
    size_t outputSize = batchSize * outputDims.c() * outputDims.h() * outputDims.w() * sizeof(float);

    CHECK(cudaMalloc(&buffers[inputIndex], inputSize));
    CHECK(cudaMalloc(&buffers[outputIndex], outputSize));

    cudaStream_t stream;
    CHECK(cudaStreamCreate(&stream));

    // DMA input batch data to device, infer on the batch asynchronously, and DMA output back to host
    CHECK(cudaMemcpyAsync(buffers[inputIndex], input, inputSize, cudaMemcpyHostToDevice, stream));

    context.enqueue(batchSize, buffers, stream, nullptr);

    CHECK(cudaMemcpyAsync(output, buffers[outputIndex], outputSize, cudaMemcpyDeviceToHost, stream));

    cudaStreamSynchronize(stream);

    cudaStreamDestroy(stream);

    CHECK(cudaFree(buffers[inputIndex]));
    CHECK(cudaFree(buffers[outputIndex]));
}



void print_mat(cv::Mat mat)
{

    std::cout << "channels : " << mat.channels()  << std::endl;
    std::cout << "depth    : " << mat.depth()     << std::endl;
    std::cout << "elemSize : " << mat.elemSize()  << std::endl;
    std::cout << "elemSize1: " << mat.elemSize1() << std::endl;

    std::cout << "total    : " << mat.total()     << std::endl;
    std::cout << "type     : " << mat.type()      << std::endl;
    std::cout << "dims     : " << mat.dims        << std::endl;
    std::cout << "flags    : " << mat.flags       << std::endl;

    std::cout << "rows     : " << mat.rows        << std::endl;
    std::cout << "cols     : " << mat.cols        << std::endl;
    std::cout << "size     : " << mat.size        << std::endl;

    std::cout << "step1    : " << mat.step1()     << std::endl;
    std::cout << "step     : " << mat.step        << std::endl;
}

int main(int argc, char** argv)
{
    std::cout << "Building and running a GPU inference engine for GoogleNet, N=4..." << std::endl;

    if(!fileExists(planFilePath))
    {
        creatGIEEngine(model, weights, planFilePath);
    }
    ICudaEngine* engine = loadGIEEngine(planFilePath);
    assert(engine != nullptr);

    IExecutionContext* context = engine->createExecutionContext();
    assert(context != nullptr);

    cv::namedWindow("Objects Detected", 1);
    std::ifstream file("test");
    while(file.getline(image_name, LINE_LENGTH))
    {
        cv::Mat mat = cv::imread(image_name);
        if(!mat.data)
        {
            fprintf(stderr, "fail\n");
            break;
        }
        cv::imshow("Objects Detected", mat);
        cv::Mat inputBlob = cv::dnn::blobFromImage(mat, 1.0, cv::Size(INPUT_W, INPUT_H), cv::Scalar(80.83, 85.08, 87.31), false, false);
        float prob[OUTPUT_SIZE];
        timeInference(*context, inputBlob.data, prob, BATCH_SIZE);
        int idx = ((prob[0] > prob[1]) ? 0 : 1);
        //fprintf(stdout, "actual value: %d, probability: %f\n", idx, prob[idx]);
	fprintf(stdout, "the class is: %s\n", idx == 0 ? "noperson" : "person");

        //if(cv::waitKey(33) == 27)
        //{
        //    break;
        //}
    }
    file.close();
    context->destroy();
    engine->destroy();
    //infer->destroy();
    //gieModelStream->destroy();
    std::cout << "Done." << std::endl;

    return 0;
}
