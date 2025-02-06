import tkinter.messagebox as msg
from tkinter import filedialog
import customtkinter as ctk
import pyperclip as ppc
import random, os, sys

global path
path = None

codes = ['#ff0000', '#ff1b00', '#ff5200', '#ff6e00', '#ffa500', '#ffa500', '#ffc300', '#ffd200',  '#fff000', '#ffff00', '#e1f707', '#c4f00e', '#89e21c', '#6cdb23', '#32cd32', '#32cd32', '#32cd32', '#32cd32', '#32cd32', '#32cd32', '#32cd32', '#32cd32', '#32cd32']

color_dict = {'red': '#ff0000',
               'orange': '#ff5200',
               'yellow': '#f5ac00',
               'green': '#0fba2e',
               'blue': '#165ea8',
               'purple': '#a302a3'}

hover_dict = {'red': '#cc0202',
              'orange': '#d94602',
              'yellow': '#d19302',
              'green': '#08751c',
              'blue': '#124982',
              'purple': '#800080'}

text_dict = {'red': 'white',
             'orange': 'white',
             'yellow': 'black',
             'green': 'white',
             'blue': 'white',
             'purple': 'white'}

lower = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n', 'm']
upper = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M']
numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
symbols = ['~', '@', '#', '$', '%', '^', '&', '*', '/', '\\', '<', '>', '-', '_', '+', '=', '|']
brackets = ['(', ')', '[', ']', '{', '}']
punctuation = [':', ',', '.', '!', '?']
lists = []

##### FILE MANAGEMENT #####
def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for PyInstaller/cx_Freeze.
    try:
        # When running as a packaged executable
        base_path = sys._MEIPASS
    except AttributeError:
        # When running in the development environment
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def writable_path(relative_path):
    # Get path to writable resource stored in user's home directory.
    user_data_dir = os.path.join(os.path.expanduser("~"), "PassGen2_Data")
    os.makedirs(user_data_dir, exist_ok=True)
    return os.path.join(user_data_dir, relative_path)

def initialize_writable_files():
    # Copy writable files to user directory if not already present.
    files_to_copy = ["settings.txt"]
    for file in files_to_copy:
        source_path = resource_path(file)
        dest_path = writable_path(file)
        if not os.path.exists(dest_path):
            try:
                with open(source_path, "r") as src, open(dest_path, "w") as dst:
                    dst.write(src.read())
            except Exception as e:
                msg.showerror('Unexpected Error!', f'(line 46) Error copying {file}: {e}')

initialize_writable_files()
########################

class tabView (ctk.CTkTabview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # create tabs
        self.add('Settings')
        self.add('Generate')
        self.add('Save')
        self.set('Generate')

        ########## tab 1 init ##########
        # widgets
        global mode
        if mode == 'dark':
            self.password_result = ctk.CTkButton( master=self.tab('Generate'), text='Click to copy', font=('Courier', 30), height=50, fg_color='transparent', hover_color='#404040', corner_radius=50, command=self.copy)
        elif mode == 'light':
            self.password_result = ctk.CTkButton( master=self.tab('Generate'), text='Click to copy', font=('Courier', 30), text_color='black', height=50, fg_color='transparent', hover_color='#B1B1B1', corner_radius=50, command=self.copy)
        self.gen_button = ctk.CTkButton(      master=self.tab('Generate'), text='Generate!', font=('helvetica',15), width=350, height=40, corner_radius=40, command=self.generate)
        self.len_label = ctk.CTkLabel(        master=self.tab('Generate'), text='Length: 16', font=('Courier', 15))
        self.len_slider = ctk.CTkSlider(      master=self.tab('Generate'), from_=6, to=30, number_of_steps=24, progress_color='white', width=300, command=self.slider_command) # remember to change progress_color depending on value (red - green)
        self.len_slider.set(16) # set default value
        self.slider_command(16) # set the length variable

        # placement
        self.password_result.grid( row=0,column=0, columnspan=2, padx=10,pady=20, sticky='ew')
        self.gen_button.grid(      row=1,column=0, columnspan=2, padx=10,pady=20)
        self.len_label.grid(       row=2,column=0,               padx=10,pady=15, sticky='e')
        self.len_slider.grid(      row=2,column=1,               padx=10,pady=15, sticky='w')
        ################################


        ########## tab 2 init ##########
        # vars for settings
        global lower_var, upper_var, numbers_var, symbols_var, punctuation_var, brackets_var
        upper_var = ctk.StringVar(value=True)
        lower_var = ctk.StringVar(value=True)
        numbers_var = ctk.StringVar(value=True)
        symbols_var = ctk.StringVar(value=True)
        punctuation_var = ctk.StringVar(value=True)
        brackets_var = ctk.StringVar(value=True)

        # widgets
        self.check_lower = ctk.CTkCheckBox(       master=self.tab('Settings'), text='Letters (lower)', variable=lower_var)
        self.check_upper = ctk.CTkCheckBox(       master=self.tab('Settings'), text='Letters (upper)', variable=upper_var)
        self.check_numbers = ctk.CTkCheckBox(     master=self.tab('Settings'), text='Numbers', variable=numbers_var)
        self.check_symbols = ctk.CTkCheckBox(     master=self.tab('Settings'), text='Symbols', variable=symbols_var)
        self.check_punctuation = ctk.CTkCheckBox( master=self.tab('Settings'), text='Punctuation', variable=punctuation_var)
        self.check_brackets = ctk.CTkCheckBox(    master=self.tab('Settings'), text='Brackets', variable=brackets_var)
        #
        self.dark_switch = ctk.CTkSwitch(             master=self.tab('Settings'), text='Dark Mode', command=self.switch_var)
        self.button_color_label = ctk.CTkLabel(       master=self.tab('Settings'), text='Button color:')
        self.button_color_dropdown = ctk.CTkComboBox( master=self.tab('Settings'), values=['red','orange','yellow','green','blue','purple'], command=self.combo_command)
        
        # set defaults
        self.check_brackets.select()
        self.check_upper.select()
        self.check_lower.select()
        self.check_numbers.select()
        self.check_punctuation.select()
        self.check_symbols.select()
        if mode == 'dark':
            self.dark_switch.select()
        elif mode == 'light':
            self.dark_switch.deselect()
        self.button_color_dropdown.set('blue')

        # placement
        self.check_upper.grid(       row=0,column=0, padx=10,pady=10, sticky='ew')
        self.check_lower.grid(       row=1,column=0, padx=10,pady=10, sticky='ew')
        self.check_numbers.grid(     row=2,column=0, padx=10,pady=10, sticky='ew')
        self.check_symbols.grid(     row=0,column=1, padx=10,pady=10, sticky='ew')
        self.check_punctuation.grid( row=1,column=1, padx=10,pady=10, sticky='ew')
        self.check_brackets.grid(    row=2,column=1, padx=10,pady=10, sticky='ew')
        #
        self.dark_switch.grid(           row=0,column=2, padx=20,pady=10, sticky='ew')
        self.button_color_label.grid(    row=1,column=2, padx=20,pady=5,  sticky='sew')
        self.button_color_dropdown.grid( row=2,column=2, padx=20,pady=5, sticky='new')
        ################################


        ########## tab 3 init ##########
        # widgets
        self.spacer = ctk.CTkLabel(       master=self.tab('Save'), text='', height=30)
        self.title_entry = ctk.CTkEntry(  master=self.tab('Save'), placeholder_text='Title', width=400)
        self.save_button = ctk.CTkButton( master=self.tab('Save'), text='Save', font=('Helvetica', 20), text_color_disabled=hover_dict[self.button_color_dropdown.get()], height=40, corner_radius=20, command=self.save, state='disabled')
        self.path_button = ctk.CTkButton( master=self.tab('Save'), text='Choose File', corner_radius=8, command=self.path)
        self.new_file = ctk.CTkButton(    master=self.tab('Save'), text='New File', corner_radius=8, command=self.makeNew)
        self.open_file = ctk.CTkButton(   master=self.tab('Save'), text='Open File', corner_radius=8, command=self.open)
        self.path_label = ctk.CTkLabel(   master=self.tab('Save'), text='no file path chosen', font=('Courier', 10))

        # placement
        self.spacer.grid(      row=0,column=0, columnspan=3, sticky='ew')
        self.title_entry.grid( row=1,column=0, columnspan=3, padx=10,pady=10, sticky='ew')
        self.save_button.grid( row=2,column=0, columnspan=3, padx=10,pady=10, sticky='nsew')
        self.path_button.grid( row=3,column=0,               padx=10,pady=10, sticky='ew')
        self.new_file.grid(    row=3,column=1,               padx=5,pady=10, sticky='ew')
        self.open_file.grid(   row=3,column=2,               padx=5,pady=10, sticky='ew')
        self.path_label.grid(  row=4,column=0, columnspan=3, padx=10,pady=10, sticky='sew')




        # set color based on file
        settings_path = writable_path('settings.txt')
        with open (settings_path, 'r') as file:
            content = file.read()
            self.combo_command(content.split(' ')[1])
            self.button_color_dropdown.set(content.split(' ')[1])

########## tab 1 functions ##########
    def copy(self):
        global mode
        temp = self.password_result.cget('text')
        if temp != 'Click to copy':
            ppc.copy(temp)
            self.password_result.configure(text='Copied!', text_color='#00FF00')
            if mode == 'dark':
                self.after(750, lambda: self.password_result.configure(text=temp, text_color='white'))
            elif mode == 'light':
                self.after(750, lambda: self.password_result.configure(text=temp, text_color='black'))

    # when the slider is updated
    def slider_command(self, value):
        global length
        if value < 10:
            self.len_label.configure(text=f'Length: 0{round(value)} ')  # update len_label
        else:
            self.len_label.configure(text=f'Length: {round(value)}')  # update len_label
        length = round(value)   # set length for password generation

        try:
            index = codes[round(value)-6]  # get the index of the color
            self.len_slider.configure(button_color=index, button_hover_color=index, progress_color=index)  # change button color depending on value
        except:
            pass

    def generate(self):
        global length, lists

        self.save_button.configure(state='normal')  # enable save button

        password = []  # reset password
        lists = []  # reset lists

        # see which lists are checked and add them to the lists list (lol)
        if lower_var.get() == '1':
            lists.extend(lower)
        if upper_var.get() == '1':
            lists.extend(upper)
        if numbers_var.get() == '1':
            lists.extend(numbers)
        if symbols_var.get() == '1':
            lists.extend(symbols)
        if punctuation_var.get() == '1':
            lists.extend(punctuation)
        if brackets_var.get() == '1':
            lists.extend(brackets)

        if len(lists) != 0:
            for i in range(length):
                password.append(random.choice(lists))
                # add characters to the list depending on length

            password_var = ''.join(password)  # convert list to string
            self.password_result.configure(text=password_var)
#####################################

########## tab 2 functions ##########
    global lower_var, upper_var, numbers_var, symbols_var, punctuation_var, brackets_var

    def combo_command(self,choice):
        def config(widget, text):
            widget.configure(fg_color=color_dict[choice])
            widget.configure(hover_color=hover_dict[choice])
            if text:
                widget.configure(text_color=text_dict[choice])
        
        config(self.gen_button,        True)

        config(self.check_brackets,    False)
        config(self.check_upper,       False)
        config(self.check_lower,       False)
        config(self.check_numbers,     False)
        config(self.check_punctuation, False)
        config(self.check_symbols,     False)

        config(self.save_button,       True)
        config(self.open_file,         True)
        config(self.new_file,          True)
        config(self.path_button,       True)

        # configure the tab button
        self.configure(segmented_button_selected_color=color_dict[choice], segmented_button_selected_hover_color=hover_dict[choice], text_color=text_dict[choice])
        # configure the switch
        self.dark_switch.configure(progress_color=color_dict[choice])

        # write in file
        settings_path = writable_path('settings.txt')
        with open (settings_path, 'r') as file:
            content = file.read()
            with open (settings_path, 'w') as file:
                file.write(content.replace(content.split(' ')[1], choice))

    def switch_var(self):
        global mode
        value = self.dark_switch.get()
        settings_path = writable_path('settings.txt')  #
        with open(settings_path, 'r') as file:         # file setup
            content = file.read()                      #
            if value == 1:
                ctk.set_appearance_mode('dark')
                self.password_result.configure(text_color='white', hover_color='#404040')
                mode = 'dark'
                with open (settings_path, 'w') as file:
                    file.write(content.replace('light','dark'))
            elif value == 0:
                ctk.set_appearance_mode('light')
                self.password_result.configure(text_color='black', hover_color='#B1B1B1')
                mode = 'light'
                with open (settings_path, 'w') as file:
                    file.write(content.replace('dark','light'))
#####################################

########## tab 3 funcitons ##########
    def save(self):
        global path
        title = self.title_entry.get()
        password = self.password_result.cget('text')

        def write():
            with open(path, 'w') as file:
                file.write(f'{title}\n')
                file.write(f'{password}\n')
                file.write('-'*40 + '\n')
            self.title_entry.delete(0, 'end')
            self.save_button.configure(text='Password Saved!', text_color='#00FF00')
            self.after(1000, lambda: self.save_button.configure(text='Save', text_color=text_dict[self.button_color_dropdown.get()]))


        if path is not None:
            write()
        else:
            self.path()
            if path is not None:
                write()
            else:
                pass

    def path(self):
        global path
        try:
            new_path = filedialog.askopenfilename(
                title="Select a File",
                filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
            )
            if new_path:
                path = new_path
        except Exception as e:
            msg.showerror("Unexpected Error!", f"error occured {e}")
        finally:
            if path is not None:
                if '.txt' not in path:
                    msg.showerror('Error!', 'Please select a .txt file')
                    path = None
            else:
                pass
            self.path_label.configure(text=f'Current path: {path}')

    def open(self):
        global path
        if path is not None:
            os.startfile(path)

    def makeNew(self):
        global path

        # make initial name
        newFileName = defaultFileName = 'passwords'
        self.new_file.configure(text='Generating file...', text_color='yellow')

        def join(name):
            newPath = os.path.join(os.path.expanduser('~/Downloads'), f'{name}.txt')
            return newPath

        # check if file is already in user's downloads
        def check():
            pathCheck = join(newFileName)
            if os.path.exists(pathCheck):
                exists = True
            else:
                exists = False
            return exists
    
        exists = check()
        if exists:
            index = 1
        while exists:
            newFileName = f'{defaultFileName}({index})'
            exists = check()
            index += 1

        # set path with new name
        newPath = join(newFileName)

        # open file and show new path
        newFile = open(newPath, 'a')
        path = newPath
        self.path_label.configure(text=f'Current path: {path}')

        # confirm to user
        def reset_confirm():
            self.new_file.configure(text='New File', text_color='white')
        self.new_file.configure(text=f'created {newFileName}', text_color='#32dc32')
        self.after(2000, reset_confirm)



class Main (ctk.CTk):
    def __init__(self):
        super().__init__()

        # setup
        self.title('PassGen 2')
        self.resizable(False, False)

        # set dark mode based on text file
        try:
            settings_path=writable_path('settings.txt')
            with open(settings_path, "r") as file:
                content = file.read()
                global mode
                if 'dark' in content:
                    ctk.set_appearance_mode('dark')
                    mode = 'dark'
                elif 'light' in content:
                    ctk.set_appearance_mode('light')
                    mode = 'light'
        except Exception as e:
            msg.showerror('Error!', f'(line 189) Could not open {settings_path}')

        # tab view
        self.tab_view = tabView(parent=self)
        self.tab_view.grid(row=0,column=0, padx=10,pady=10)

app = Main()
app.mainloop()
os._exit(0)
