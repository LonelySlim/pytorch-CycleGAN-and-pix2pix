import os
from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim

def get_image_lists(directory):
    real_A_list = []
    fake_B_list = []

    for filename in os.listdir(directory):
        if filename.endswith("_real_A.png"):
            real_A_list.append(filename)
        elif filename.endswith("_fake_B.png"):
            fake_B_list.append(filename)
    
    # 对列表进行排序
    real_A_list.sort()
    fake_B_list.sort()

    return real_A_list, fake_B_list

def calculate_psnr(original, reconstructed):
    mse = np.mean((original - reconstructed) ** 2)
    if mse == 0:
        return float('inf')
    PIXEL_MAX = 255.0
    psnr = 20 * np.log10(PIXEL_MAX / np.sqrt(mse))
    return psnr

def calculate_ssim(original, reconstructed):
    ssim_value = ssim(original, reconstructed, data_range=reconstructed.max() - reconstructed.min(), multichannel=True, channel_axis=-1)
    return ssim_value

# 设置你的文件夹路径
directory_path = './results/usenhance_cyclegan/test_latest/images/'

# 获取图片列表
real_A_list, fake_B_list = get_image_lists(directory_path)

PSNR = []
SSIM = []

for i in range(len(real_A_list)):
    # 使用 Pillow 读取原始图像和重建图像
    original_image = np.array(Image.open(directory_path + real_A_list[i]))
    reconstructed_image = np.array(Image.open(directory_path + fake_B_list[i]))

    # 确保图像大小相同
    if original_image.shape != reconstructed_image.shape:
        raise ValueError("Input images must have the same dimensions.")

    # 计算 PSNR
    psnr_value = calculate_psnr(original_image, reconstructed_image)
    #print(f"PSNR: {psnr_value} dB")
    PSNR.append(psnr_value)

    # 计算 SSIM
    ssim_value = calculate_ssim(original_image, reconstructed_image)
    #print(f"SSIM: {ssim_value}")
    SSIM.append(ssim_value)

# 打印结果
#print("Real A images:", real_A_list)
#print("Fake B images:", fake_B_list)

# 计算 PSNR 的均值和方差
psnr_mean = np.mean(PSNR)
psnr_variance = np.var(PSNR)

# 计算 SSIM 的均值和方差
ssim_mean = np.mean(SSIM)
ssim_variance = np.var(SSIM)

#print(PSNR)
#print(SSIM)
#print(f"PSNR Mean: {psnr_mean}")
#print(f"PSNR Variance: {psnr_variance}")
#print(f"SSIM Mean: {ssim_mean}")
#print(f"SSIM Variance: {ssim_variance}")

# 准备要写入文件的内容
output_content = (
    f"PSNR Mean: {psnr_mean}\n"
    f"PSNR Variance: {psnr_variance}\n"
    f"SSIM Mean: {ssim_mean}\n"
    f"SSIM Variance: {ssim_variance}\n"
)

# 将结果写入文件
output_file_path = directory_path + 'calculate_index.txt'
with open(output_file_path, 'w') as file:
    file.write(output_content)

print(f"Results written to {output_file_path}")
