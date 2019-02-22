#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 08:52:09 2019

@author: swec
"""

#import Tkinter, tkFileDialog
#
#win= Tkinter.Tk()
#
#win.title('Data augmentation with bounding boxes')
#win.directory_destin= tkFileDialog.askdirectory(title=' name of the folder where the new images and data files need to be saved')
#win.directory_original= tkFileDialog.askdirectory(title=' directory of the orignal data')
#
##win.mainloop()

from Tkinter import *
from imgaug_fullfolder import image_augment_function as img_sam
import tkMessageBox
import tkFileDialog



class Checkbar(Frame):
   def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
      Frame.__init__(self, parent)
      self.vars = []
      for pick in picks:
         var = BooleanVar()
         var.set(True)
         chk = Checkbutton(self, text=pick, variable=var)
         chk.pack(side=side, anchor=anchor, expand=YES)
         self.vars.append(var)
   def state(self):
      return map((lambda var: var.get()), self.vars)
  
def browse_button_input():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path_input
    filename = tkFileDialog.askdirectory()
    folder_path_input=(filename)
    print(filename)
    
def browse_button_output():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path_output
    filename = tkFileDialog.askdirectory()
    folder_path_output=(filename)
    print(filename)
  
if __name__ == '__main__':
   root = Tk()
   Label(root, text="Number of augmentations per picture").pack()
   augmentations = Entry(root)
   augmentations.insert(0,'10')
   augmentations.pack()
   
   button2 = Button(text="Select directory where the original images can be found", command=browse_button_input).pack()
   button3 = Button(text="Select directory where the new images and data files need to be saved", command=browse_button_output).pack()
      
   var_bb = BooleanVar()
   var_bb.set(True)
   safe_bb_images = Checkbutton(root, text='Save bounding box images', variable=var_bb)
   safe_bb_images.pack()
   dataoptions = Label(root, text="Data augmentation options")
   dataoptions.pack()
   fields1=['Crop' , 'Affine' , 'Superpixel' , 'Blur'  
          , 'Sharpen' , 'Emboss' , 'Superpixel' , 'Blur' 
          , 'EdgeDetect' , 'AdditiveGaussianNoise' ]
   fields2=['OneOf' , 'Add' 
          , 'Multiply' , 'ContrastNormalization' 
          , 'Grayscale' , 'ElasticTransformation' 
          ,'PiecewiseAffine' ]
   fields=fields1+fields2
   lng = Checkbar(root, fields1)
   tgl = Checkbar(root, fields2)
   lng.pack(fill=X)
   tgl.pack(fill=X)

   def allstates(): 
      selector= dict(zip(fields, list(lng.state())+list(tgl.state())))
      augm=int(augmentations.get())
      #name of the folder where the new images and data files need to be saved
      directory_name_new=folder_path_output+'/'
      #directory of the orignal data
      directory = folder_path_input+'/'
      savebb=var_bb.get()
      #tkMessageBox.showinfo('information','augmentation is ongoing, please do not close the app')
      img_sam(augm,savebb,directory_name_new,directory,selector)
      tkMessageBox.showinfo('information','augmentation finished, the app will close when you push ok')      
      root.destroy()
   Label(root, text="Start the process").pack()
   Button(root, text='Start', command=allstates).pack()
   Button(root, text='Quit', command=root.destroy).pack()
   root.mainloop()

