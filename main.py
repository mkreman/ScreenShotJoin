from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.colorchooser import askcolor
import tkinter.font as font_list
from PIL import Image
import webbrowser
from database import *


def browse_images():
    filenames = filedialog.askopenfilenames(initialdir=os.path.join(os.path.expanduser('~'), 'Pictures'),
                                            title="Select Images",
                                            filetypes=(("Images", "*.png *.jpg *.jpeg *.bmp"), ("All Files", "*.*")))

    # It returns a tuple of selected files
    return list(filenames)


class App:
    def __init__(self):
        self.changes = None
        self.variables = None
        self.browse_images_button = None
        self.images = None
        self.image_string = None
        self.image_list = None
        self.list_box = None
        self.direction_var = None
        self.main_panel = None
        self.bg_color = 'bg_color'
        self.button_bg_color = 'button_bg_color'
        self.fg_color = 'fg_color'
        self.font = 'font'
        self.output_dir = 'output_dir'

    def options(self):
        options_window = Toplevel(bg=self.variables[self.bg_color])
        options_window.title('Options')
        logo = PhotoImage(file='images/logo.png')
        options_window.iconphoto(False, logo)

        self.changes = []

        Label(master=options_window,
              text="Window's Background Color",
              font=(self.variables[self.font], 14),
              bg=self.variables[self.bg_color]).grid(row=0, column=0, padx=10, pady=5, sticky=E)
        windows_bg_color = Button(master=options_window,
                                  bd=1,
                                  fg=self.variables[self.fg_color],
                                  font=(self.variables[self.font], 12),
                                  text='Pick Color',
                                  bg=self.variables[self.button_bg_color],
                                  command=lambda: [windows_bg_color.config(bg=self.askcolor_window(self.bg_color))])
        windows_bg_color.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        Label(master=options_window,
              text="Button's Background Color",
              font=(self.variables[self.font], 14),
              bg=self.variables[self.bg_color]).grid(row=1, column=0, padx=10, pady=5, sticky=E)
        button_bg_color = Button(master=options_window,
                                 bd=1,
                                 fg=self.variables[self.fg_color],
                                 font=(self.variables[self.font], 12),
                                 text='Pick Color',
                                 bg=self.variables[self.button_bg_color],
                                 command=lambda:
                                 [button_bg_color.config(bg=self.askcolor_window(self.button_bg_color))])
        button_bg_color.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        Label(master=options_window,
              text="Font",
              font=(self.variables[self.font], 14),
              bg=self.variables[self.bg_color]).grid(row=2, column=0, padx=10, pady=5, sticky=E)

        button_font_value = StringVar(value=self.variables[self.font])
        button_font_drop = OptionMenu(options_window, button_font_value, *font_list.families())
        button_font_drop.config(font=(self.variables[self.font], 12),
                                bd=1,
                                bg=self.variables[self.button_bg_color])
        button_font_drop.grid(row=2, column=1, padx=10, pady=5, sticky=W)
        button_font_drop["menu"]["background"] = self.variables[self.bg_color]
        for x in range(0, int(button_font_drop['menu'].index('end'))):
            button_font_drop['menu'].entryconfig(x, font=font_list.Font(family=font_list.families()[x]))
        button_font_drop["menu"]["activeborderwidth"] = '2'

        directions = ["Vertical", "Horizontal"]

        Label(master=options_window,
              bg=self.variables[self.bg_color],
              fg=self.variables[self.fg_color],
              font=(self.variables[self.font], 14),
              text="Choose Orientation").grid(row=3, column=0, padx=10, pady=5, sticky=E)

        button_font_drop = OptionMenu(options_window, self.direction_var, *directions)
        button_font_drop.config(bg=self.variables[self.button_bg_color],
                                font=(self.variables[self.font], 12),
                                bd=1,
                                fg=self.variables[self.fg_color])
        button_font_drop.grid(row=3, column=1, padx=10, pady=5, sticky=W)
        button_font_drop["menu"]["background"] = self.variables[self.bg_color]
        for x in range(len(directions)):
            button_font_drop['menu'].entryconfig(x, font=(self.variables[self.font], 14))
        button_font_drop["menu"]["activeborderwidth"] = '2'

        Label(master=options_window,
              bg=self.variables[self.bg_color],
              fg=self.variables[self.fg_color],
              font=(self.variables[self.font], 14),
              text=f"Current Output Directory").grid(row=4, column=0, padx=10, pady=5, sticky=E)

        output_dir_label = Label(master=options_window,
                                 bg=self.variables[self.bg_color],
                                 fg='gray',
                                 font=('Cambria', 10),
                                 text='...'+self.variables[self.output_dir][-30:])
        output_dir_label.grid(row=5, column=0, padx=10, pady=5, sticky=E)

        Button(master=options_window,
               bg=self.variables[self.button_bg_color],
               fg=self.variables[self.fg_color],
               font=(self.variables[self.font], 12),
               bd=1,
               text="Change Directory",
               command=lambda: [output_dir_label.config(text='...'+self.change_output_dir()[-30:])])\
            .grid(row=4, column=1, padx=10, pady=5, sticky=W)

        Button(master=options_window,
               bg=self.variables[self.button_bg_color],
               fg=self.variables[self.fg_color],
               font=(self.variables[self.font], 12),
               bd=2,
               height=1,
               width=6,
               text="Save",
               command=lambda: [self.change_values()]).grid(row=6, column=0, columnspan=2, padx=5, pady=10)

        options_window.grab_set()
        options_window.mainloop()

    def combine_images(self, image_path, direction, output_dir):
        if not image_path:
            return
        elif len(image_path) == 1:
            messagebox.showerror("Error", "Please select more than one image")
            return
        images = [Image.open(x) for x in image_path]
        widths, heights = zip(*(i.size for i in images))

        if direction == "Horizontal":
            x_offset = 0
            y_offset = 0
            total_width = sum(widths)
            max_height = max(heights)

            new_im = Image.new('RGB', (total_width, max_height))

            for im in images:
                new_im.paste(im, (x_offset, y_offset))
                x_offset += im.size[0]

            file_name = os.path.join(output_dir, image_path[0].split('/')[-1].split('.')[0] + '_joined.png')
            while os.path.exists(file_name):
                file_name = file_name[:-11] + '_' + file_name[-11:]
            new_im.save(file_name)
        elif direction == "Vertical":
            x_offset = 0
            y_offset = 0
            total_height = sum(heights)
            max_width = max(widths)

            new_im = Image.new('RGB', (max_width, total_height))

            for im in images:
                new_im.paste(im, (x_offset, y_offset))
                y_offset += im.size[1]

            file_name = os.path.join(output_dir, image_path[0].split('/')[-1].split('.')[0] + '_joined.png')
            while os.path.exists(file_name):
                file_name = file_name[:-11] + '_' + file_name[-11:]
            new_im.save(file_name)
        messagebox.showinfo("Success", "Combined image is saved!")
        self.clear_list_box()

    def run(self):
        self.main_panel = Tk()
        self.main_panel.title('Screen Shot Join')
        logo = PhotoImage(file='images/logo.png')
        self.main_panel.iconphoto(False, logo)
        
        self.variables = get_variable_values()
        # Creating Menubar
        menu_bar = Menu(self.main_panel)
        # File menu
        file_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=file_menu)

        file_menu.add_command(label='Options', command=self.options)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=lambda: [self.main_panel.destroy()])

        self.main_panel.config(bg=self.variables[self.bg_color], menu=menu_bar)

        self.direction_var = StringVar(value="Horizontal")
        if not os.path.exists(os.path.join(os.path.expanduser('~'), 'Pictures', 'ScreenShotJoin')):
            os.mkdir(os.path.join(os.path.expanduser('~'), 'Pictures', 'ScreenShotJoin'))

        first_frame = Frame(self.main_panel, bg=self.variables[self.bg_color])
        Label(master=first_frame,
              bg=self.variables[self.bg_color],
              fg=self.variables[self.fg_color],
              font=(self.variables[self.font], 14),
              text="Join Images").grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        second_frame = Frame(self.main_panel, bg=self.variables[self.bg_color])

        self.browse_images_button = Button(master=second_frame,
                                           bg=self.variables[self.button_bg_color],
                                           fg=self.variables[self.fg_color],
                                           font=(self.variables[self.font], 14),
                                           bd=2,
                                           text='Browse Images',
                                           command=lambda: [self.list_of_images(browse_images())])
        self.browse_images_button.grid(row=1, column=0, padx=5, pady=5)

        first_frame.pack(side='top')
        second_frame.pack(side='top')
        self.main_panel.geometry('550x150')
        self.main_panel.mainloop()

    def move_up(self):
        idx = self.list_box.curselection()
        if not idx:
            return
        pos = idx[0]
        if pos != 0:
            text = self.list_box.get(pos)
            self.list_box.delete(pos)
            self.list_box.insert(pos - 1, text)
            self.images.pop(pos)
            self.images.insert(pos - 1, text)
            self.list_box.selection_set(pos - 1)

    def move_down(self):
        idx = self.list_box.curselection()
        if not idx:
            return
        pos = idx[0]
        if pos != len(self.images) - 1:
            text = self.list_box.get(pos)
            self.list_box.delete(pos)
            self.list_box.insert(pos+1, text)
            self.images.pop(pos)
            self.images.insert(pos+1, text)
            self.list_box.selection_set(pos + 1)

    def delete(self):
        idx = self.list_box.curselection()
        if not idx:
            return
        pos = idx[0]
        self.list_box.delete(pos)
        self.images.pop(pos)

    def list_of_images(self, images):
        self.browse_images_button.config(state=DISABLED)
        self.images = images
        image_list = [image.split('/')[-1] for image in self.images]
        third_frame = Frame(self.main_panel, bg=self.variables[self.bg_color])

        button_frame = Frame(third_frame, bg=self.variables[self.bg_color])
        image_list_frame = Frame(third_frame, bg=self.variables[self.bg_color])

        minus_button_image = PhotoImage(file='./images/minus.png')
        Button(master=button_frame,
               bg=self.variables[self.button_bg_color],
               bd=0,
               image=minus_button_image,
               command=lambda: [self.delete()]).pack(side=RIGHT)
        plus_button_image = PhotoImage(file='./images/plus.png')
        Button(master=button_frame,
               bg=self.variables[self.button_bg_color],
               bd=0,
               image=plus_button_image,
               command=lambda: [self.add_more_images()]).pack(side=RIGHT)
        down_button_image = PhotoImage(file='./images/down.png')
        Button(master=button_frame,
               bg=self.variables[self.button_bg_color],
               bd=0,
               image=down_button_image,
               command=lambda: [self.move_down()]).pack(side=RIGHT)
        up_button_image = PhotoImage(file='./images/up.png')
        Button(master=button_frame,
               bg=self.variables[self.button_bg_color],
               bd=0,
               image=up_button_image,
               command=lambda: [self.move_up()]).pack(side=RIGHT)

        scrollbar_y = Scrollbar(image_list_frame)
        scrollbar_y.pack(side='right', fill='y')

        self.image_string = StringVar(value=image_list)
        self.list_box = Listbox(master=image_list_frame,
                                listvariable=self.image_string,
                                selectmode="single",
                                yscrollcommand=scrollbar_y.set,
                                font=(self.variables[self.font], 14))
        self.list_box.pack(side='top', padx=10, pady=10, fill="both", expand=True)

        button_frame.pack(side='top', padx=35, pady=10, fill='x')
        image_list_frame.pack(side='top', fill='both', expand=True)

        self.main_panel.geometry('550x550')
        third_frame.pack(side='top', padx=10, pady=10, fill='both', expand=True)

        fourth_frame = Frame(self.main_panel, bg=self.variables[self.bg_color])
        Button(master=fourth_frame,
               bg=self.variables[self.button_bg_color],
               fg=self.variables[self.fg_color],
               font=(self.variables[self.font], 14),
               bd=2,
               text="Merge",
               command=lambda: [self.combine_images(self.images,
                                                    self.direction_var.get(),
                                                    self.variables[self.output_dir])]).pack(side='left', padx=5)

        Button(master=fourth_frame,
               bg=self.variables[self.button_bg_color],
               fg=self.variables[self.fg_color],
               font=(self.variables[self.font], 14),
               bd=2,
               text="Open Output Folder",
               command=lambda: [webbrowser.open(self.variables[self.output_dir])]).pack(side='left', padx=5)

        fourth_frame.pack(side='top', pady=10)
        third_frame.mainloop()
        fourth_frame.mainloop()

    def add_more_images(self):
        new_images = list(browse_images())
        self.images += new_images
        for img in new_images:
            self.list_box.insert(END, img.split('/')[-1])

    def change_output_dir(self):
        new_path = filedialog.askdirectory(initialdir=self.variables[self.output_dir])
        if new_path:
            self.changes.append((self.output_dir, new_path))
            return new_path
        return self.output_dir

    def clear_list_box(self):
        for _ in range(len(self.images)):
            self.list_box.delete(0)
        self.images = []

    def askcolor_window(self, variable):
        color = askcolor(title="Choose Color")
        if color[1] is not None:
            self.changes.append((variable, color[1]))
            return color[1]
        return self.variables[variable]

    def change_values(self):
        if messagebox.askokcancel("Warning!", "In order to save the changes, Application must be restarted.\n" +
                                              "Are you sure, you want to continue..."):
            for variable, value in self.changes:
                Database.update_meta_value(variable, value)
            restart_application(self.main_panel)


def restart_application(window):
    window.destroy()
    new_instance = App()
    new_instance.run()


if __name__ == '__main__':
    app_instance = App()
    app_instance.run()
