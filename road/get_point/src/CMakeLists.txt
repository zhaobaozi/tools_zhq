cmake_minimum_required(VERSION 3.5)
project(usb_cam)
find_package(catkin REQUIRED COMPONENTS
  cv_bridge
  image_transport
  roscpp
  sensor_msgs
  std_msgs
)
find_package(OpenCV REQUIRED)
find_package(PCL)
 
include_directories(
  ${catkin_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
  ${PCL_INCLUDE_DIRS}
)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
add_executable(get_point get_point.cpp)
 
target_link_libraries(get_point ${catkin_LIBRARIES} ${OpenCV_LIBS} ${PCL_LIBRARIES})
