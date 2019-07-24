#include<ros/ros.h>
#include<pcl/point_cloud.h>
#include<pcl_conversions/pcl_conversions.h>
#include<sensor_msgs/PointCloud2.h>
#include<pcl/io/pcd_io.h>//which contains the required definitions to load and store point clouds to PCD and other file formats.
#include<iostream>
#include<fstream>
#include<string>
#include<cstring>
#include <sstream>
#include <pcl/ModelCoefficients.h>  
#include <pcl/io/pcd_io.h>                 
#include <pcl/point_types.h>             
#include <pcl/sample_consensus/method_types.h> 
#include <pcl/sample_consensus/model_types.h>    
#include <pcl/segmentation/sac_segmentation.h>  
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <fstream>
#include <pcl_ros/point_cloud.h>
#include <pcl/io/pcd_io.h>
#include "std_msgs/String.h"   
#include <pcl/io/pcd_io.h>   
#include <pcl/search/kdtree.h>
#include <pcl/ModelCoefficients.h>
#include <pcl/point_types.h>
#include <pcl/io/pcd_io.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/features/normal_3d.h>
#include <pcl/kdtree/kdtree.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/segmentation/extract_clusters.h>  
using namespace std;
double stringToNum(const string& str)
{
    istringstream iss(str);
    double num;
    iss >> num;
    return num;
}
int main(int argc, char **argv){
    ros::init (argc, argv, "view_pcd");
    ros::NodeHandle nh;
    ros::Publisher pcl_pub = nh.advertise<sensor_msgs::PointCloud2> ("pcl_output", 1);
    pcl::PointCloud<pcl::PointXYZ> cloud;
    sensor_msgs::PointCloud2 output;
    // 定义输入文件流类对象infile
    ifstream infile("/home/zhaohuaqing/Documents/do_some_try/road/data/hongcao_1.txt",ios::in);
 
    if(!infile){  // 判断文件是否存在
      cerr<<"open error."<<endl;
      exit(1); // 退出程序
    }
 
    char str[255]; // 定义字符数组用来接受读取一行的数据
    int count=0;
    while(count<15073)
    {   
        count=count+1;
        pcl::PointXYZ tmp_new;
        infile.getline(str,255);  // getline函数可以读取整行并保存在str数组里
        string aa(str);
        string temp(aa,0,13);
        std::cout<<"ha1----:"<<endl;
        std::cout<<"ha1----:"<<temp<<endl;
        double x= stringToNum(temp);
        tmp_new.x=x-347877.407694;
        string temp1(aa,15,14);
        std::cout<<"ha----:"<<endl;
        double y= stringToNum(temp1);
        tmp_new.y=y-3450730.025276;
        string temp2(aa,31,10);
        double z= stringToNum(temp2);
        tmp_new.z=z;
        //tmp_new.intensity=z;
        cloud.push_back(tmp_new);
        std::cout<<"size----:"<<cloud.points.size()<<std::endl;
    }
    pcl::io::savePCDFile<pcl::PointXYZ>("./1.pcd", cloud);
    return 1;
}

