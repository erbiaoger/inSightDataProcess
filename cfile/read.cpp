#include <libmseed.h>
#include <stdio.h>

static flag verbose = 0;
static flag ppackets = 0;
static flag basicsum = 0;
static int printdata = 0;
static int reclen = -1;
static char *inputfile = 0;


int main()
{
    
    MSRecord *msr = NULL;

    // 打开 MSEED 文件并读取数据
    int nrecs = ms_readmsr(&msr, "data.mseed", reclen, NULL, NULL, 1,
                                printdata, verbose);
    
    //msr_print(msr, 0);
    int data = msr_unpack_data(msr, 0, verbose);

    printf("%d", data);
    // 释放内存
    // ms3_freeRecord(msr, 1, 0);
}