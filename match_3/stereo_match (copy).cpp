#include <opencv2/opencv.hpp>
#include <iostream>
#include <fstream>
#include <math.h>
using namespace cv;
using namespace std;
int x_r,y_r;
double fx;
double baseline;
double x_first,y_first,z_first;

class Compute_Depth
{
private:

	Mat rectifyImageL, rectifyImageR;
	Mat Rl, Rr, Pl, Pr, Q;             
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
    cameraMatrixL = (Mat_<double>(3, 3) <<1.7142773645020914e+03, 0., 7.5568348772302852e+02, 0.,
       1.7173786645251278e+03, 5.2443539227999054e+02, 0., 0., 1.  );
    distCoeffL = (Mat_<double>(5, 1) << -4.6671246804779054e-01, 4.2052789113647621e-01,
       -8.7601122899133698e-03, -1.1373937510866353e-02,
       -5.3547932679464094e-01);
//右相机内参
    cameraMatrixR = (Mat_<double>(3, 3) <<1.7135055105542831e+03, 0., 6.7947027185644845e+02, 0.,
       1.7169262678268931e+03, 5.2670961424182542e+02, 0., 0., 1.  );
    distCoeffR = (Mat_<double>(5, 1) << -4.9374353085204986e-01, 3.8213544872437522e-01,
       -3.6567113051621941e-03, 5.4880277969571213e-03,
       -2.9049001760810045e-01);
//左右相机之间的R/T,左×R+T=右
    R = (Mat_<double>(3, 3) << 9.9744726732364719e-01, 2.6311336822980873e-03,
       7.1358433588011139e-02, -3.9224224322589006e-03,
       9.9983098123384495e-01, 1.7961725062746316e-02,
       -7.1299112973806561e-02, -1.8195771500891449e-02,
       9.9728900043499713e-01 );
    T = (Mat_<double>(3, 1) <<-1.5320187814465277e+02, -3.3037700311049627e-02,4.5780820011901069e+00);
    fx =cameraMatrixL.at<double>(0, 0);
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
      std::cout<<"x/R:"<<x_r<<" "<<"y/R:"<<y_r<<std::endl;     
    }
  }
//获取左图所选点坐标，并与右图点做计算求三维点
  static void On_mouse_L(int event, int x, int y, int flags, void*)
  {
    
    if (event == EVENT_LBUTTONDOWN) 
    {   
      static int count_left=0;
			count_left=count_left+1;
      static Point recent_Point = Point(x, y);
      std::cout<<"x/L:"<<x<<" "<<"y/L:"<<y<<std::endl;  
      int disparity_pixel=x-x_r;
      std::cout<<"disparity_pixel:"<<disparity_pixel<<std::endl;  
      double depth=baseline*fx/disparity_pixel;
      double x_camera=x*depth/fx;
      double y_camera=y*depth/fx;
      std::cout<<"x_c:"<<x_camera<<" "<<"y_c:"<<y_camera<<" "<<"z_c:"<<depth<<std::endl; 
//第二次选取点对的时候，计算两点之间的误差
      if(count_left%2==0)
      {
          double result=sqrt((x_camera-x_first)*(x_camera-x_first)+(y_camera-y_first)*(y_camera-y_first)+(depth-z_first)*(depth-z_first));
          std::cout<<"---------result(fx*b/d)单位（m）-------:"<<result/1000.0<<std::endl;

       }
      x_first=x_camera;
      y_first=y_camera;
      z_first=depth;
        
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
{ 	Compute_Depth A("/home/zhaohuaqing/Documents/tools/save_Synchron_img/img_bottom/left_img/left20.jpg","/home/zhaohuaqing/Documents/tools/save_Synchron_img/img_bottom/right_img/right20.jpg");
    A.get_depth(); 
    return 0;
}

