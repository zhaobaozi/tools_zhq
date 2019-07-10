cmake_minimum_required(VERSION 3.5.2)
project(match_3)

set(CMAKE_CXX_STANDARD 11)
find_package(OpenCV REQUIRED) 
add_executable(stereo_match stereo_match.cpp)
include_directories( ${OpenCV_INCLUDE_DIRS})
target_link_libraries(stereo_match ${OpenCV_LIBS})
