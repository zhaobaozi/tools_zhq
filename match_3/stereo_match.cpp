#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>
#include <math.h>
using namespace cv;
using namespace std;
int x_r,y_r;
double fx,fy;
double baseline;
double u0,v0;
double x_first,y_first,z_first;
vector<Point2f> pts_1, pts_2;
Mat Pl, Pr;
class Compute_Depth
{
private:

	Mat rectifyImageL, rectifyImageR;
	Mat Rl, Rr, Q;             
	Mat mapLx, mapLy, mapRx, mapRy;  
	int imageWidth ;                   
	int imageHeight; 
	Rect validROIL;
	Rect validROIR;
  Mat rgbImageL, grayImageL;
  Mat rgbImageR, grayImageR;
  Size imageSize;
  Mat cameraMatrixL,cameraMatrixR;
  Mat distCoeffL,distCoeffR;
  Mat R,T;

public:

  Compute_Depth(string left_img,string right_img)
  {
    rgbImageL = imread(left_img,CV_LOAD_IMAGE_COLOR);
    rgbImageR = imread(right_img, CV_LOAD_IMAGE_COLOR);
    imageWidth=rgbImageR.cols;
    imageHeight=rgbImageR.rows;
    imageSize= Size(imageWidth, imageHeight);
//左相机内参
    cameraMatrixL = (Mat_<double>(3, 3) <<3.7912622241517342e+03, 0., 6.9737279479548397e+02, 0.,
       3.7926803591110975e+03, 5.8906325499534194e+02, 0., 0., 1.  );
    distCoeffL = (Mat_<double>(5, 1) << -4.0698233082950569e-01, -9.3493541513714256e+00,
       -1.2764178023578496e-03, 3.5848585766711264e-03,
       1.6919014459061904e+02);
//右相机内参
    cameraMatrixR = (Mat_<double>(3, 3) <<3.7747355484116779e+03, 0., 7.0197851844667503e+02, 0.,
       3.7752669822455837e+03, 5.8210092107801154e+02, 0., 0., 1. );
    distCoeffR = (Mat_<double>(5, 1) <<-4.6024818550370422e-01, -4.2263597910563337e+00,
       -1.8649876558347897e-05, 4.6225867587901042e-03,
       7.1573365239765849e+01);
//左右相机之间的R/T,左×R+T=右
    R = (Mat_<double>(3, 3) << 9.9979601021459918e-01, 1.3829728065510340e-03,
       -2.0150070600009853e-02, -1.1550263284688181e-03,
       9.9993526316536252e-01, 1.1319690481537161e-02,
       2.0164420972336027e-02, -1.1294107518241517e-02,
       9.9973288395561788e-01 );
    T = (Mat_<double>(3, 1) <<-1.5340313347444746e+02, -1.8134126864255118e-01,
       -2.6733784648301224e+00);
    fx =cameraMatrixL.at<double>(0, 0);
    fy =cameraMatrixL.at<double>(1, 1);
    u0=cameraMatrixL.at<double>(0, 2);
    v0=cameraMatrixL.at<double>(1, 2);

//基线长度
    baseline =T.at<double>(0, 0)*10*(-1);
  }
//获取右图所选点坐标
  static void On_mouse_R(int event, int x, int y, int flags, void*)
  {
    
    if (event == EVENT_LBUTTONDOWN) 
    {
      Point recent_Point= Point(x, y);
      x_r=recent_Point.x;  
      y_r=recent_Point.y;
      //std::cout<<"x/R:"<<x_r<<" "<<"y/R:"<<y_r<<std::endl;     
    }
  }
//获取左图所选点坐标，并与右图点做计算求三维点。有f*b/d和triangulatePoints两种方法
  static void On_mouse_L(int event, int x, int y, int flags, void*)
  {
    
    if (event == EVENT_LBUTTONDOWN) 
    {   
      static int count_left=0;
			count_left=count_left+1;
      static Point recent_Point = Point(x, y);
      //std::cout<<"x/L:"<<x<<" "<<"y/L:"<<y<<std::endl;  
      int disparity_pixel=x-x_r;
      double depth=baseline*fx/disparity_pixel;
      double x_camera=(x-u0)*depth/fx;
      double y_camera=(y-v0)*depth/fy;
      if(count_left%2==1)//获取右图坐标
      {
        pts_1.push_back(Point2f(x,y));
        pts_2.push_back(Point2f(x_r,y_r));
        x_first=x_camera;
        y_first=y_camera;
        z_first=depth;
        std::cout<<"---------begin(f*b/d)单位（m）-------:"<<std::endl;
        std::cout<<"x_1:"<<x_first/1000<<" "<<"y_1:"<<y_first/1000<<" "<<"z_1:"<<z_first/1000<<std::endl; 
       }
      if(count_left%2==0)//获取左图坐标
      {
        double result=sqrt((x_camera-x_first)*(x_camera-x_first)+(y_camera-y_first)*(y_camera-y_first)+(depth-z_first)*(depth-z_first));
        std::cout<<"x_2:"<<x_camera/1000<<" "<<"y_2:"<<y_camera/1000<<" "<<"z_2:"<<depth/1000<<std::endl; 
        std::cout<<"---------result(f*b/d)单位（m）-------:"<<result/1000.0<<std::endl;

        pts_1.push_back(Point2f(x,y));
        pts_2.push_back(Point2f(x_r,y_r));
        Mat pts_4d;
        cv::triangulatePoints( Pl, Pr, pts_1, pts_2, pts_4d);
        float first_x,first_y,first_z,second_x,second_y,second_z;
        first_x=pts_4d.at<float>(0,0)/pts_4d.at<float>(3,0);
        first_y=pts_4d.at<float>(1,0)/pts_4d.at<float>(3,0);
        first_z=pts_4d.at<float>(2,0)/pts_4d.at<float>(3,0);
        second_x=pts_4d.at<float>(0,1)/pts_4d.at<float>(3,1);
        second_y=pts_4d.at<float>(1,1)/pts_4d.at<float>(3,1);
        second_z=pts_4d.at<float>(2,1)/pts_4d.at<float>(3,1);
        std::cout<<"---------begin_triangulate单位（m）-------:"<<std::endl;
        std::cout<<"x_11:"<<first_x/100<<"  y_11:"<<first_y/100<<"  z_11:"<<first_z/100<<std::endl;
        std::cout<<"x_22:"<<second_x/100<<"  y_22:"<<second_y/100<<"  z_22:"<<second_z/100<<std::endl;
        double result_2=sqrt((first_x-second_x)*(first_x-second_x)+(first_y-second_y)*(first_y-second_y)+(first_z-second_z)*(first_z-second_z));
        std::cout<<"---------triangulate_result单位（m）-------:"<<result_2/100<<std::endl;
        pts_1.erase(pts_1.begin(),pts_1.end());
        pts_2.erase(pts_2.begin(),pts_2.end());
       }

        
    }
  }
//对原图去畸变＋基线校正
  void get_depth()
  {
    stereoRectify(cameraMatrixL, distCoeffL, cameraMatrixR, distCoeffR, imageSize, R, T, Rl, Rr, Pl, Pr, Q, CALIB_ZERO_DISPARITY,
		0, imageSize, &validROIL, &validROIR);
    initUndistortRectifyMap(cameraMatrixL, distCoeffL, Rl, Pr, imageSize, CV_32FC1, mapLx, mapLy);
    initUndistortRectifyMap(cameraMatrixR, distCoeffR, Rr, Pr, imageSize, CV_32FC1, mapRx, mapRy);
    cvtColor(rgbImageL, grayImageL, CV_BGR2GRAY);
    cvtColor(rgbImageR, grayImageR, CV_BGR2GRAY);
    remap(grayImageL, rectifyImageL, mapLx, mapLy, INTER_LINEAR);
    remap(grayImageR, rectifyImageR, mapRx, mapRy, INTER_LINEAR);
    Mat rgbRectifyImageL, rgbRectifyImageR;
    cvtColor(rectifyImageL, rgbRectifyImageL, CV_GRAY2BGR);  
    cvtColor(rectifyImageR, rgbRectifyImageR, CV_GRAY2BGR);

    imshow("ImageL After Rectify", rgbRectifyImageL);
    imshow("ImageR After Rectify", rgbRectifyImageR);
    setMouseCallback("ImageL After Rectify", On_mouse_L);
    setMouseCallback("ImageR After Rectify", On_mouse_R);
    Mat canvas;
    double sf;
    int w, h;
    sf = 600. / MAX(imageSize.width, imageSize.height);
    w = cvRound(imageSize.width * sf);
    h = cvRound(imageSize.height * sf);
    canvas.create(h, w * 2, CV_8UC3);   								
    Mat canvasPart = canvas(Rect(w * 0, 0, w, h));                              
    resize(rgbRectifyImageL, canvasPart, canvasPart.size(), 0, 0, INTER_AREA);   
    Rect vroiL(cvRound(validROIL.x*sf), cvRound(validROIL.y*sf),           
	  cvRound(validROIL.width*sf), cvRound(validROIL.height*sf));
    cout << "Painted ImageL" << endl;
    canvasPart = canvas(Rect(w, 0, w, h));                                
    resize(rgbRectifyImageR, canvasPart, canvasPart.size(), 0, 0, INTER_LINEAR);
    Rect vroiR(cvRound(validROIR.x * sf), cvRound(validROIR.y*sf),
		cvRound(validROIR.width * sf), cvRound(validROIR.height * sf));
    cout << "Painted ImageR" << endl;
    for (int i = 0; i < canvas.rows; i += 16)
        line(canvas, Point(0, i), Point(canvas.cols, i), Scalar(0, 255, 0), 1, 8);
    imshow("rectified", canvas);

    waitKey(0);
  }
};

int main()
{ 	Compute_Depth A("/home/zhaohuaqing/Documents/tools/save_Synchron_img/img_top/left_img/left18.jpg","/home/zhaohuaqing/Documents/tools/save_Synchron_img/img_top/right_img/right18.jpg");
    A.get_depth(); 
    return 0;
}

