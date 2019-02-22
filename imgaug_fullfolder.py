#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 12:05:34 2019

@author: swec
"""
import imgaug as ia
import matplotlib.pyplot as plt
import img_aug_seq
import skimage
import os


def image_augment_function(n_augmentations,save_image_boundingbox,directory_name_new,directory,selector):
    print('start of image augmentations')
    seq=img_aug_seq.image_augmentation(selector)        
    iterations=0 # to display the progress
    for filename in os.listdir(directory):    
        if filename.endswith(".png"): 
            print(iterations)
            iterations += 1
            #open image
            image=skimage.io.imread(directory+filename)
            
            #find the corresponding text file and open it
            name_of_txtfile=directory+filename[0:-3]+'txt'
            lines = open(name_of_txtfile).read().splitlines()
            #extract the different bounding boxes
            bbs_ind=[None] * len(lines)
            for i in range(len(lines)):
                indiv_data=lines[i].split()
                bbs_ind[i] = ia.BoundingBox(x1=float(indiv_data[4]), y1=float(indiv_data[5]), x2=float(indiv_data[6]), y2=float(indiv_data[7]))
                    
            bbs = ia.BoundingBoxesOnImage(bbs_ind, shape=image.shape)
            name_img=filename[0:-3]
            #do the data augmentation
            for i in range(n_augmentations):
                seq_det = seq.to_deterministic()
                # Augment BBs and images.
                # As we only have one image and list of BBs, we use
                # [image] and [bbs] to turn both into lists (batches) for the
                # functions and then [0] to reverse that. In a real experiment, your
                # variables would likely already be lists.
                image_aug = seq_det.augment_images([image])[0]
                bbs_aug = seq_det.augment_bounding_boxes([bbs])[0]
                #save the image
                skimage.io.imsave(directory_name_new+ name_img + '_' +str(i)+ '.png', image_aug)
                #save the image with bounding box
                if save_image_boundingbox:
                    image_after = bbs_aug.draw_on_image(image_aug, thickness=2, color=[0, 0, 255])      
                    skimage.io.imsave(directory_name_new+ name_img + '_' +str(i)+ 'bb.png', image_after)
                    
                #save new text file
                new_data=''
                for j in range(len(lines)):
                    new_data_obj1=lines[j].split()
                    new_data_obj1[4]=str(bbs_aug.bounding_boxes[j].x1)
                    new_data_obj1[5]=str(bbs_aug.bounding_boxes[j].y1)
                    new_data_obj1[6]=str(bbs_aug.bounding_boxes[j].x2)
                    new_data_obj1[7]=str(bbs_aug.bounding_boxes[j].y2)
                    new_data_obj1=' '.join(new_data_obj1)
                    new_data=new_data+new_data_obj1+'\n'
                file_data = open(directory_name_new+ name_img + '_' +str(i)+ '.txt','w+')
                file_data.write(new_data)
                file_data.close()
  

if __name__ == '__main__':
    #how many extra figure do you want to create from 1 figure
    n_augmentations=10
    #also save the image with bounding box?
    save_image_boundingbox=True
    #name of the folder where the new images and data files need to be saved
    directory_name_new='/home/swec/imageaugmentation/imagefolder/'
    #directory of the orignal data
    directory = '/home/swec/imageaugmentation/testdata/'
    
    selector={'Crop' : True, 'Affine' : True, 'Superpixel' : True, 'Blur' : True 
              , 'Sharpen' : True, 'Emboss' : True, 'Superpixel' : True, 'Blur' : True
              , 'EdgeDetect' : True, 'AdditiveGaussianNoise' : True
              , 'OneOf' : True, 'Add' : True
              , 'Multiply' : True, 'ContrastNormalization' : True
              , 'Grayscale' : True, 'ElasticTransformation' : True
              ,'PiecewiseAffine' : True}
    image_augment_function(n_augmentations,save_image_boundingbox,directory_name_new,directory,selector)          

## image with BBs before/after augmentation (shown below)
#image_before = bbs.draw_on_image(image, thickness=2)
#image_after = bbs_aug.draw_on_image(image_aug, thickness=2, color=[0, 0, 255])
#plt.subplot(2,1,1)
#plt.imshow(image_before)
#plt.subplot(2,1,2)
#plt.imshow(image_after)