#include <iostream>
#include <fstream>
#include <string>
#include <iomanip>
#include <vector>
#include <pcl_ros/point_cloud.h>
#include <pcl/io/pcd_io.h>
#include "cv.h"
typedef unsigned char uchar;
struct PointXYZ
{
    double x, y, z;
};

/*
  Author:chd_ayj
  Date:2018-6-8
  Description: read .PCD file
*/

//读取pcd点云文件
void readPCDfile(const std::string finname, std::vector<PointXYZ>& points, const std::string foutname)
{
    std::ifstream fin(finname);
    if (fin.bad()){
        std::cout << "打开文件失败！" << std::endl;
        return;
    }

    char s[11][1024]; //存储Header
    int Points_Num; //点数量
    std::string data_columns_type; //列数: X Y Z
    std::string data_type; //点坐标存储方式(ascii或者binary)
    pcl::PointCloud<pcl::PointXYZ> cloud_point_all;
    pcl::PointCloud<pcl::PointXYZ> cloud_point_all2;
    std::vector<PointXYZ> cloud;
    //连续读取Header行数
    std::cout << "start to read file header....." << std::endl;
    std::cout << "file header: " << std::endl;
    for (int i = 0; i < 11; ++i){
        fin.getline(s[i], 1024);
        //std::cout << "第" << i + 1 << "行：" << s[i] << std::endl;
        std::cout << s[i] << std::endl;

        //FIELDS x y z rgb
        if (i == 2){
            std::string s2 = s[2];
            size_t pos = s2.find("FIELDS");
            size_t size = s2.size();
            data_columns_type = s2.substr(pos + 7, size);
            //std::cout << "data_columns_type:" << data_columns_type << std::endl;
        }

        //POINTS xxx
        if (i == 9){
            std::string s9 = s[9], Points_Str;
            size_t pos = s9.find("POINTS");
            size_t size = s9.size();
            Points_Str = s9.substr(pos + 7, size);
            Points_Num = atoi(Points_Str.c_str());
            //std::cout << "Points:" << std::Points_Num << endl;
        }

        //DATA ascii或者binary
        if (i == 10){
            std::string s10 = s[10], DATA_SIZE;
            size_t pos = s10.find("DATA");
            size_t size = s10.size();
            data_type = s10.substr(pos + 5, size);
            //std::cout << "data_type:" << data_type << std::endl;
        }
    }
    std::cout << std::endl;
    std::cout << "start to read point ....." << std::endl;
    PointXYZ p;
    if ((data_columns_type == "x y z") && (data_type == "ascii")){
        //读取点坐标记录
        while (!fin.eof()){
            
            fin >> p.x >> p.y >> p.z;
            if (fin.peek() == EOF){
                break;
            }
            //1
            //std::cout<<"hahaha"<<std::endl;
            cloud.push_back(p);
        }
    }else{
        std::cout << "data_type = binary, read failed!" << std::endl;
    }
    //步骤一
    int count_1=0;
    for(int i=0;i < cloud.size(); ++i)
    {
    bool delet=false;
    double Time1 = (double)cvGetTickCount();

    std::cout<<"i_1:"<<i<<std::endl;
        double x,y,x1,y1;
        uchar p2=0,p3=0,p4=0,p5=0,p6=0,p7=0,p8=0,p9=0;
        int p2_count=0,p3_count=0,p4_count=0,p5_count=0,p6_count=0,p7_count=0,p8_count=0,p9_count=0;
        int min,max;
        if(i<500){
        min=0;
        max=i+500;
        }
        else if(i>(cloud.size()-500)){
        min=i-500;
        max=cloud.size();
        }
        else if(i>500 or i<cloud.size()-500){
        min=i-500;
        max=i+500;
        }
        for(int j=min;j < max; ++j){
            x=cloud.at(i).x;
            y=cloud.at(i).y;
            x1=cloud.at(j).x;
            y1=cloud.at(j).y;
            //std::cout<<"x-x1:"<<x-x1<<std::endl;
            if(((x-0.03)<= x1) && (x1<= (x+0.03)) && ((y-0.09)<=y1) && (y1<y) && (i!=j)){//2
                p2_count=p2_count+1;
                //std::cout<<"here2"<<std::endl;
            }
            if((x<= x1) && (x1<= (x+0.09)) && (y-0.03)<y1 && (y1<(y+0.03)) && (i!=j)){//4
                p4_count=p4_count+1;
                //std::cout<<"here4"<<std::endl;
            }
            if(((x-0.03)<= x1) && (x1<= (x+0.03)) && (y<=y1) && (y1<=(y+0.09))&& (i!=j)){//6
                //p6_count=p6_count+1;H
                //std::cout<<"here6"<<std::endl;
            }
            if(((x-0.09)<= x1)&& (x1<= x) && ((y-0.03)<=y1) && (y1<=(y+0.03))&& (i!=j)){//8
                p8_count=p8_count+1;
                //std::cout<<"here8"<<std::endl;
            }
         }
            if(p2_count>=1){
                p2=1;
            }

            if(p4_count>=1){
                p4=1;
            }

            if(p6_count>=1){
                p6=1;
            }

            if(p8_count>=1){
                p8=1;
            }

            if((p2 + p4+ p6  + p8 ) >= 2 && (p2 + p4+ p6  + p8 ) <= 3){
                if (p2 * p4 * p6 == 0 && p4 * p6 * p8 == 0)
                {
                    //标记
                    std::cout<<"删除啦！"<<std::endl;
                    delet=true;
                    count_1=count_1+1;
                    std::cout<<"count_1_delet:"<<count_1<<std::endl;
                }

            
        }
        if(delet==false){
            pcl::PointXYZ tmp_new;
            tmp_new.x=cloud.at(i).x;
            tmp_new.y=cloud.at(i).y;
            tmp_new.z=cloud.at(i).z;
            cloud_point_all.push_back(tmp_new);
        }
        Time1 = (double)cvGetTickCount() - Time1;
        //printf( "run time1 = %gms\n", Time1 /(cvGetTickFrequency()*1000) );//毫秒
    }
    int count_2=0;
    for(int i=0;i<cloud_point_all.points.size();i++)
    {   std::cout<<"i_2:"<<i<<std::endl;
        double x_,y_,x1_,y1_;
        bool delet1=false;

        uchar p2_=0,p3_=0,p4_=0,p5_=0,p6_=0,p7_=0,p8_=0,p9_=0;
        int p2_count_=0,p3_count_=0,p4_count_=0,p5_count_=0,p6_count_=0,p7_count_=0,p8_count_=0,p9_count_=0;
        int min_,max_;
        if(i<500){
        min_=0;
        max_=i+500;
        }
        else if(i>(cloud_point_all.points.size()-500)){
        min_=i-500;
        max_=cloud_point_all.points.size();
        }
        else if(i>500 or i<cloud_point_all.points.size()-500){
        min_=i-500;
        max_=i+500;
        }
        for(int j=min_;j < max_; ++j){
            x_=cloud_point_all.points[i].x;
            y_=cloud_point_all.points[i].y;
            x1_=cloud_point_all.points[j].x;
            y1_=cloud_point_all.points[j].y;
            if(((x_-0.03)<= x1_) && (x1_<= (x_+0.03)) && ((y_-0.09)<=y1_) && (y1_<y_) && (i!=j)){//2
                p2_count_=p2_count_+1;
                //std::cout<<"here2__2"<<std::endl;
            }
            if((x_<= x1_) && (x1_<= (x_+0.09)) && (y_-0.03)<y1_ && (y1_<(y_+0.03)) && (i!=j)){//4
                p4_count_=p4_count_+1;
                //std::cout<<"here4___2"<<std::endl;
            }
            if(((x_-0.03)<= x1_) && (x1_<= (x_+0.03)) && (y_<=y1_) && (y1_<=(y_+0.09))&& (i!=j)){//6
                p6_count_=p6_count_+1;
                //std::cout<<"here6__2"<<std::endl;
            }
            if(((x_-0.09)<= x1_)&& (x1_<= x_) && ((y_-0.03)<=y1_) && (y1_<=(y_+0.03))&& (i!=j)){//8
                p8_count_=p8_count_+1;
                //std::cout<<"here8__3"<<std::endl;
             }
            }
            if(p2_count_>=1){
                p2_=1;
            }

            if(p4_count_>=1){
                p4_=1;
            }

            if(p6_count_>=1){
                p6_=1;
            }

            if(p8_count_>=1){
                p8_=1;
            }

            if ((p2_ + p4_+ p6_  + p8_ ) >= 2 && (p2_ + p4_+ p6_  + p8_ ) <= 3)
            {

                if ( p2_ * p4_ * p8_ == 0 && p2_ * p6_ * p8_ == 0)
                {
                    //标记
                    std::cout<<"删除啦,2！"<<std::endl;
                    delet1=true;
                    count_2=count_2+1;
                    std::cout<<"count_2_delet:"<<count_2<<std::endl;
                }

            
        }
       if(delet1==false){
           pcl::PointXYZ tmp_new1;
           tmp_new1.x=cloud_point_all.points[i].x;
           tmp_new1.y=cloud_point_all.points[i].y;
           tmp_new1.z=cloud_point_all.points[i].z;
           cloud_point_all2.push_back(tmp_new1);
        }
    }
    ////////////////////////////////////////////////////////////
    //点坐标输出txt文本
    std::cout << "start to write new points to pcd....." << std::endl;
    std::cout<<"cloud_point_all2.size():"<<cloud_point_all2.points.size()<<std::endl;
    pcl::io::savePCDFile<pcl::PointXYZ>("/home/zhaohuaqing/Downloads/cowa/3d_xihua_percetion/catkin_ws/cloud_point_all_new712_500_xihua.pcd", cloud_point_all2);

    std::cout << "write point to txt finished!" << std::endl;
}

int main()
{
    std::string finname = "/home/zhaohuaqing/zhq/tf/cloud_point_all_new712_500.pcd";
    std::string foutame = "new_xyz_711.pcd";
    std::vector<PointXYZ> points;
    readPCDfile(finname, points, foutame);

    return 0;
}
