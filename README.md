# Under-Water-Image-Super-Resolution


## Problem Statement: 
Given an underwater low-resolution degraded image, we initially enhance the image to remove degradation effects and then improve the quality of image by super resolution.

The proposed methodology of enhancing and super resolving of UW images consists of three main modules.
<br/>
![alt text](https://github.com/BasavarajMS11/Under-Water-Image-Super-Resolution/blob/master/Images/methodology.jpg?raw=true)
<br/>
1. Image Enhancement(IE)
2. Image Super Resolution(ISR)
3. Performance Evaluation(PE)

Initially the input degraded low resolution UW image is enhanced by IE by recovering all underwater degradation effects.
Then the enhanced UW image is super resolved using SR module. At the end PSNR and SSIM are found for generated output with the ground truth.

## 1. Image Enhancement(IE):

### 1.1 Modified-Image Formation Model(IFM)
This is the physics based model to enhance UW degraded image using IFM equation. 
Here we used a modified equation from IBLA by reversing the process for UW degraded images.
- To get recovered image run the file  /Code/IFM/main.py by providing path of input images(LRD).
- The results stored in save directory folder set in the code.

### 1.2 Modified-Unsupervised Color Correction Method (UCM) 
This is the prior based color correction technique for correcting the degraded UW image.
- Run the file /Code/UCM/main.py to obtain color corrected UW images.
- Set input directory to LRD image and results are stored in output directory.

### Fusion of IFM and UCM:
Since the fusion technique performs better than the sequential approach the results obtained from 1.1 and 1.2 are fused to obtain intermediate enhanced image 
stored in specific folder for further enhancing and super resolving. 
- Run /Code/Fusion/Blend.py file to obtain fusion of IFM and UCM output.

### 1.3 GAN Based IE
This is GAN based image enhancement technique to further enhance intermediate enhanced image obtained by fusion.
#### Training:
- FUnIEGAN architecture used to train the model.
- The model can be trained on existing paired data sets such as EUVP and UFO against the GT.
- We trained the model on UFO 120 dataset with the dimension of 256 x 256.
- The hyperameters can be tuned using YAML files in /Code/FUnIEGAN/config directory.
- To train the model on train dataset run /Code/FUnIEGAN/train_funie.py

#### Testing:
- Run /Code/FUnIEGAN/test.py to test on test images.
- Set the path to trained generator of FUnIEGAN model in the test.py file.
- Enhanced UW images can be found in output directory set.

## 2. Image Super Resolution
This is GAN based image SR for super resolving enhanced UW image.
#### Training:
- SRDRM architecture is used to super resolve enhanced UW image.
- The model can be trained on UW SR datasets such as UFO-120 and USR-248.
- We trained the model using UFO-120 dataset at scale of 2x
- The dimensions of input image is 256 x 256 and output dimension of 512 x 512.
- The hyperparameters can be tuned while training.
- To train the model run /Code/SRDRM/train_genarative_models_2x.py.

#### Testing: 
- Run /Code/SRDRM/test_SR_2x.py to test on test images.
- Set the path to trained generator of SRDRM model in the test_SR_2x.py file.
- Super resolved UW images can be found in output directory set.

## 3. Performance Evaluation(PE)
- Run /Code/PE/measure.py to find PSNR and SSIM quality metric for performance measure.
- Set the generated results and ground truth path to measure PSNR and SSIM measures.


## Results
