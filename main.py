import os
import tkinter
import os.path as osp
from PIL import Image, ImageTk

class DirInfo():
    def __init__(self, tag, abs_path):
        self.tag = tag # tag for visualization, which is used to distinguish images under different directories
        self.abs_path = abs_path # image folder absolute path

    def __nozero__(self):
        return osp.exists(self.abs_path)

class ShowStamp():
    def __init__(self, dir_index, image_index, num_dirs, num_images):
        self.dir_index = dir_index  # Index of the currently displayed directory
        self.image_index = image_index # Index of the currently displayed image
        self.num_dirs = num_dirs # total dir number
        self.num_images = num_images # total image number

    def next_dir(self):
        self.dir_index = (self.dir_index + 1) % self.num_dirs

    def next_image(self):
        self.dir_index = 0
        self.image_index = (self.image_index + 1) % self.num_images

    def forehead_image(self):
        self.dir_index = 0
        self.image_index = ((self.image_index - 1) + self.num_images) % self.num_images

def is_image(file_name):
    if file_name.endswith('.bmp') or file_name.endswith('.png') or \
            file_name.endswith('.jpg') or file_name.endswith('.jpeg'):
        return True
    else:
        return False

class ImageCompareGUI():
    def __init__(self, dir_infos):
        """ init gui configuration

        :param dir_infos: DirInfo list
        """
        self.init_window = tkinter.Tk()
        self.dir_infos = dir_infos
        self.num_dirs = len(self.dir_infos)
        self.image_names = self.get_inter_image_names()
        self.num_images = len(self.image_names)

        self.show_stamp = ShowStamp(0, 0, self.num_dirs, self.num_images)

    def set_init_window(self):
        self.init_window.title("高分辨率图像对比可视化工具")
        init_image = self.get_image()
        self.canvas = tkinter.Button(self.init_window, image=init_image, command=self.dir_switch)
        self.canvas.grid(row=0, column=0, columnspan=3)
        self.forehead = tkinter.Button(self.init_window, text="上一张", command=self.forehead_image_switch)
        self.forehead.grid(row=1, column=0)
        self.next = tkinter.Button(self.init_window, text="下一张", command=self.next_image_switch)
        self.next.grid(row=1, column=2)

    def get_inter_image_names(self):
        """ Get a list of image names that are contained in all directories

        :return: str list, each element is a image_name
        """
        inter_image_names = []
        for index, dir_info in enumerate(self.dir_infos):
            curdir_image_names = []
            for file_name in os.listdir(dir_info.abs_path):
                if is_image(file_name):
                    curdir_image_names.append(file_name)
            if index == 0:
                inter_image_names = curdir_image_names
            else:
                inter_image_names = list(set(inter_image_names).union(set(curdir_image_names)))

        return inter_image_names

    def get_image(self):
        """ Return the image to be displayed according to the self.show_stamp

        :return: ImageTk.PhotoImage
        """
        current_dir = self.dir_infos[self.show_stamp.dir_index].abs_path
        current_image_path = osp.join(current_dir, self.image_names[self.show_stamp.image_index])
        image = Image.open(current_image_path)
        return ImageTk.PhotoImage(image)

    def dir_switch(self):
        """ Change the directory to the next one, but do not change the image name, and update canvas
        """
        self.show_stamp.next_dir()
        self.update_canvas()

    def forehead_image_switch(self):
        """ Change the image to the forehead one and reset the directory to the first one, and update canvas
        """
        self.show_stamp.forehead_image()
        self.update_canvas()

    def next_image_switch(self):
        """ Change the image to the next one and reset the directory to the first one, and update canvas
        """
        self.show_stamp.next_image()
        self.update_canvas()

    def update_canvas(self):
        """ Change the image on the canvas according to the self.show_stamp
        """
        current_image = self.get_image()
        self.canvas.configure(image=current_image)









