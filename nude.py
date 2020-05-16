import sys
import os
import _io
from collections import namedtuple
from PIL import Image

class Nude:
    Skin = namedtuple("Skin", "id skin region x y")

    def __init__(self, path_or_image):
#若 Path_or_image 为 Image.Image类型的实例，直接赋值，若为str类型的实例，则打开图片
    if isinstance(path_or_image, Image.Image):
        self.image = path_or_image
    elif isinstance(path_or_image, str):
        self.image = Image.open(path_or_image)

# 获得图片所有颜色通道
    bands = self.image.getbands()
# 判断是否为单通道图片（即灰度图），是则将灰度图转为RGB图
    if len(bands) == 1:
# 新建相同大小的RGB图像
        new_img = Image.new("RGB", self.image.size)
# 拷贝灰度图到RGB图(PIL自动进行颜色通道转换）
        new_img.paste(self.image)
        f = self.image.filename
# 替换self.image
        self.image = new_img
        self.image.filename = f

# 存储对应图像所有像素的全部 Skin 对象
        self.skin_map = []
# 检测到的皮肤区域，元素的索引即为皮肤区域号，元素都是包含一些Skin对象的列表
        self.detected_region = []
# 元素区域号代表的都是待合并的区域
        self.merge_regions = []
# 整合后的皮肤区域
        self.skin_region = []
# 最近合并的两个皮肤区域的区域号，初始化都为-1
        self.last_from, self.last_to = -1, -1
# 色情图片判断结果
        self.result = None
# 处理得到的信息
        self.message = None
# 图像宽和高
        self.width, self.height = self.image.size
# 图像总像素
        self.total_pixels = self.width * self.height

