#!/bin/bash
# by yinzhedfs
#4、下载下来的是swf文件,需要转换成pdf
#https://github.com/yinzhedfs/swf2pdf
#brew install swftools
#brew install imagemagick
#然后按照github上边的步骤就行

work_dir=$1               # 工作目录
dest_dir="pdfFiles"       # 转换后的pdf存放目录
png_tmp_dir="png"         # swf生成的临时png文件目录
logs_dir="logs"           # 日志目录
x_axis="2480"             # png图片长边像素
y_axis="3508"             # png图片宽边像素
count=0                   # 转换文件计数
thread_nums=4             # 线程数


function swf_convert(){
    echo "The $count SWF file is converting ..."
    filename=$1
    count=$2
    swfrender -X $x_axis -Y $y_axis $work_dir/$filename -o $png_tmp_dir/$count.png 2>>$logs_dir/swfrender_err.log
}
if [ ! -d $work_dir/$dest_dir ];then
    mkdir $work_dir/png
    mkdir $work_dir/logs

fi
for swf in `ls $work_dir | grep swf` ;do
    cd $work_dir
    # 判断线程数量
    swfrender_threads=`ps aux| grep "swfrender"| grep -v 'grep'| wc -l`
    while [ "$swfrender_threads" -ge "$thread_nums" ];do
        sleep 1
        swfrender_threads=`ps aux| grep "swfrender"| grep -v 'grep'| wc -l`
    done
    count=$[count+1]
    swf_convert $swf $count &
    sleep 1
done

# 等待子进程结束
wait
echo -e "\n=================================="
echo "$count SWF files converted done!"
