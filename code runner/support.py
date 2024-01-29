from os import walk #helps going through the contents of a folder and looking at each file one by one 
import pygame

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):  # we've got the entire path of our code to our img #we get to access all of our img files 
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
        
        
    return surface_list   # we're importing them and putting 'em into a surface we're putting the entire list of surfaces at the end of the function
