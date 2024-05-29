依赖详见requirements.txt。

数据集可见于datasets/usenhance文件夹，其中trainA文件夹为训练用低质量图像，trainB文件夹为训练用高质量图像，testA文件夹为测试用低质量图像，testB文件夹为测试用高质量图像。

训练好的模型位于checkpoints/usenhance_cyclegan文件夹中，其中latest_net_G_A.pth是由低质量图像生成高质量图像的生成器，也是我们最终需要的模型。

测试结果可见于results/usenhance_cyclegan/test_latest文件夹，使用浏览器打开index.html文件即可查看。对于其中的每一行图片，real_A为低质量图片，fake_B为模型由低质量图片生成的高质量图片，real_B为高质量图片。

如何训练模型：python train.py --dataroot ./datasets/usenhance --name usenhance_cyclegan --model cycle_gan

如何测试模型：python test.py --dataroot ./datasets/usenhance --name usenhance_cyclegan --model cycle_gan --num_test 208