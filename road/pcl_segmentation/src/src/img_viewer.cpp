#include<ros/ros.h>
#include<pcl/point_cloud.h>
#include<pcl_conversions/pcl_conversions.h>
#include<sensor_msgs/PointCloud2.h>
#include<pcl/io/pcd_io.h>
#include<iostream>
#include<fstream>
#include<string>
#include<cstring>
#include <sstream>            
#include <pcl/point_types.h>             
#include <pcl/sample_consensus/method_types.h> 
#include <pcl/sample_consensus/model_types.h>    
#include <pcl_conversions/pcl_conversions.h>
#include <pcl_ros/point_cloud.h>
#include "std_msgs/String.h"   
#include <pcl/filters/extract_indices.h>
#include <pcl/features/normal_3d.h>
#include <pcl/kdtree/kdtree.h>
#include <pcl/segmentation/extract_clusters.h>  
using namespace std;
int main(int argc, char **argv){
	ros::init (argc, argv, "view_pcd");
	ros::NodeHandle nh;
	ros::Publisher pcl_pub = nh.advertise<sensor_msgs::PointCloud2> ("pcl_output", 1);
	sensor_msgs::PointCloud2 output;
	pcl::PCDReader reader;
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>), cloud_f (new pcl::PointCloud<pcl::PointXYZ>);
	reader.read ("/home/zhaohuaqing/Downloads/cowa/tf/catkin_ws/1.pcd", *cloud);
  pcl::search::KdTree<pcl::PointXYZ>::Ptr tree (new pcl::search::KdTree<pcl::PointXYZ>);
  tree->setInputCloud (cloud); //创建点云索引向量，用于存储实际的点云信息
	std::vector<pcl::PointIndices> cluster_indices;
	pcl::EuclideanClusterExtraction<pcl::PointXYZ> ec;
  pcl::PCDWriter writer;
	ec.setClusterTolerance (2.5); //设置近邻搜索的搜索半径为2.5m
	ec.setMinClusterSize (100);//设置一个聚类需要的最少点数目为100
	ec.setMaxClusterSize (25000); //设置一个聚类需要的最大点数目为25000
	ec.setSearchMethod (tree);//设置点云的搜索机制
	ec.setInputCloud (cloud);
	ec.extract (cluster_indices);//从点云中提取聚类，并将点云索引保存在cluster_indices中
	int j = 0;
	for (std::vector<pcl::PointIndices>::const_iterator it = cluster_indices.begin (); it != cluster_indices.end (); ++it)
	{
		pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_cluster (new pcl::PointCloud<pcl::PointXYZ>);
		//创建新的点云数据集cloud_cluster，将所有当前聚类写入到点云数据集中
		for (std::vector<int>::const_iterator pit = it->indices.begin (); pit != it->indices.end (); ++pit)
			 cloud_cluster->points.push_back (cloud->points[*pit]); //*
		cloud_cluster->width = cloud_cluster->points.size ();
		cloud_cluster->height = 1;
		cloud_cluster->is_dense = true;

		std::cout << "PointCloud representing the Cluster: " << cloud_cluster->points.size () << " data points." << std::endl;
		std::stringstream ss;
		ss << "cloud_cluster_" << j << ".pcd";
		writer.write<pcl::PointXYZ> (ss.str (), *cloud_cluster, false); //*
		j++;
	}
    return 1;
}


