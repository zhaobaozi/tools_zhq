#include<ros/ros.h>
#include<sensor_msgs/PointCloud2.h>
#include<iostream>
#include<fstream>
#include<string>
#include<cstring>
#include <sstream>
#include <pcl/ModelCoefficients.h>                
#include <pcl/point_types.h>             
#include <pcl/sample_consensus/method_types.h> 
#include <pcl/sample_consensus/model_types.h>    
#include <pcl_ros/point_cloud.h>
#include<pcl/point_cloud.h>
#include<pcl_conversions/pcl_conversions.h>
#include "std_msgs/String.h"    
#include <pcl/search/kdtree.h>
#include <pcl/io/pcd_io.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/features/normal_3d.h>
#include <pcl/kdtree/kdtree.h>
#include <pcl/segmentation/extract_clusters.h>  
#include <pcl/common/common.h>
#include<opencv2/opencv.hpp>
using namespace std;
class Grid//将一个栅格定义为一个类对象
{
public:
	double h_mean=0;//平均高度
	pcl::PointCloud<pcl::PointXYZ> grid_cloud;//每个删格里的点云
	int num=0;//点云个数
};

int stringToNum(const string& str)
{
	istringstream iss(str);
	int num;
	iss >> num;
	return num;
}
int main(int argc, char **argv)
{
	string pcl_path;
	string img_save_path;
	string txt_path;
  int have_point;
	pcl_path=argv[1];
	img_save_path=argv[2];
	have_point=atoi(argv[3]);
	txt_path=argv[4];
	pcl::PointCloud<pcl::PointXYZRGB> malu_all;
	ros::init (argc, argv, "view_pcd");
	ros::NodeHandle nh;
	ros::Publisher pcl_pub = nh.advertise<sensor_msgs::PointCloud2> ("pcl_output", 1);
	sensor_msgs::PointCloud2 output;
	pcl::PCDReader reader;
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
	reader.read (pcl_path, *cloud);
	pcl::PointXYZ min;//用于存放三个轴的最小值
	pcl::PointXYZ max;//用于存放三个轴的最大值
	pcl::getMinMax3D(*cloud,min,max);
	//std::cout<<"min:"<<min<<std::endl;
	//std::cout<<"max:"<<max<<std::endl;
	double grid_size_x=0.05;
	double grid_size_y=0.05;//栅栏化5cm
	int row=int((max.y-min.y)/grid_size_y);
	int column=int((max.x-min.x)/grid_size_x);
	Grid grid[row][column];
	int j=0;
	int i=0;
	cv::Mat src_gray;
	src_gray = cv::Mat::zeros(row, column, CV_64F);
	for (int m=0;m<cloud->size();m++)
	{
		for( i=0;i<row;i++)
		{
			if ((((cloud->points[m].y-min.y)>=i*grid_size_y)&&((cloud->points[m].y-min.y)<=i*grid_size_y+grid_size_y)))//如果x在某范围内
			{
				for( j=0;j<column;j++)
				{
					if(((cloud->points[m].x-min.x)>=j*grid_size_x)&&((cloud->points[m].x-min.x)<=j*grid_size_x+grid_size_x))//如果y在某范围内
					{   
						grid[i][j].num=grid[i][j].num+1;
						grid[i][j].h_mean=int((grid[i][j].h_mean+(cloud->points[m].z-min.z)/(max.z-min.z)*255)/grid[i][j].num);
						src_gray.at<double>(i,j)=grid[i][j].h_mean;
						pcl::PointXYZ tmp_new;
						tmp_new.x=cloud->points[m].x;
						tmp_new.y=cloud->points[m].y;
						tmp_new.z=cloud->points[m].z;
						grid[i][j].grid_cloud.push_back(tmp_new);//得到每个栅栏里的点云
					}               
				}           
			}       
		}   
	} 
	cv::imwrite(img_save_path,src_gray);//存点云对应的二维图  

	if(have_point)
	{
		ifstream infile(txt_path,ios::in);
		char str[255];
		for( int i = 0; i < cloud->size(); i++) 
		{
			pcl::PointXYZRGB tmp_new_2;
			tmp_new_2.x=cloud->points[i].x;
			tmp_new_2.y=cloud->points[i].y;
			tmp_new_2.z=cloud->points[i].z;
			tmp_new_2.r = 255;
			tmp_new_2.g = 255;
			tmp_new_2.b = 255;
			malu_all.push_back(tmp_new_2);
		}
		while(infile.getline(str,255))
		{   

			pcl::PointXYZ tmp_new;
			string aa(str);
			string temp(aa,0,2);
			int x= stringToNum(temp);
			string temp1(aa,3,2);
			int y= stringToNum(temp1);
			for( int i = 0; i < grid[x][y].grid_cloud.points.size(); i++) 
			{
				pcl::PointXYZRGB tmp_new_1;
				tmp_new_1.x=grid[x][y].grid_cloud.points[i].x;
				tmp_new_1.y=grid[x][y].grid_cloud.points[i].y;
				tmp_new_1.z=grid[x][y].grid_cloud.points[i].z;
				tmp_new_1.r = 255;
				tmp_new_1.g = 0;
				tmp_new_1.b = 0;
				malu_all.push_back(tmp_new_1);
			}
		}
		std::cout<<"malu_all.size:"<<malu_all.points.size()<<std::endl;
		pcl::toROSMsg(malu_all,output);
		output.header.frame_id = "odom";
		ros::Rate loop_rate(1);
		while (ros::ok())
		{
			pcl_pub.publish(output);
			ros::spinOnce();
			loop_rate.sleep();
		}		
	}

		return 1;
}





