## 1
data中放置需要进行马路牙子提取的点云数据块（分割后的pcd）
## 2
- **./run_get_point.sh** 
注意修改参数，首次运行HAVE_POINT修改为0。这个过程将点云投影为二维图像，并保存在result中。
## 3
- **.run_img_process.sh** 
对投影的二维图像进行处理，提取二维马路牙子，根据不同的二维图像，可能需要调整阈值，即MEDIAN_THRESHOLD和MASK_THRESHOLD，图像可在result查看。
## 4
- **./run_get_point.sh** 
再次运行，需要修改HAVE_POINT为1，运行成果后可以在rviz中观察。

## 注意 ##
由于x,y数据较大，使用过程中的数据已经分别减去347877.407694和3450730.025276
