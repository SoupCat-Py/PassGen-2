import tkinter.messagebox as msg
import customtkinter as ctk
import pyperclip as ppc
import random, os, sys

codes = ['#ff0000', '#ff1b00', '#ff5200', '#ff6e00', '#ffa500', '#ffa500', '#ffc300', '#ffd200',  '#fff000', '#ffff00', '#e1f707', '#c4f00e', '#89e21c', '#6cdb23', '#32cd32', '#32cd32', '#32cd32', '#32cd32', '#32cd32', '#32cd32', '#32cd32', '#32cd32', '#32cd32']

colour_dict = {'red': '#ff0000',
               'orange': '#ff5200',
               'yellow': '#fff000',
               'green': '#32dc32',
               'blue': '#1a5694',
               'purple': '#a302a3'}

hover_dict = {'red': '#cc0202',
              'orange': '#d94602',
              'yellow': '#c2b502',
              'green': '#21b021',
              'blue': '#114070',
              'purple': '#800080'}

text_dict = {'red': 'white',
             'orange': 'white',
             'yellow': 'black',
             'green': 'black',
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

###########################

class tabView (ctk.CTkTabview):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # create tabs
        self.add('Generate')
        self.add('Settings')

        # tab 1 widgets
        global mode
        if mode == 'dark':
            self.password_result = ctk.CTkButton( master=self.tab('Generate'), text='Click to copy', font=('Courier', 30), height=50, fg_color='transparent', hover_color='#404040', corner_radius=50, command=self.copy)
        elif mode == 'light':
            self.password_result = ctk.CTkButton( master=self.tab('Generate'), text='Click to copy', font=('Courier', 30), text_color='black', height=50, fg_color='transparent', hover_color='#B1B1B1', corner_radius=50, command=self.copy)
        self.gen_button = ctk.CTkButton(      master=self.tab('Generate'), text='Generate!', font=('helvetica',15), width=350, height=40, corner_radius=40, command=self.generate)
        self.len_label = ctk.CTkLabel(        master=self.tab('Generate'), text='Length: 16', font=('Courier', 15))
        self.len_slider = ctk.CTkSlider(      master=self.tab('Generate'), from_=6, to=30, number_of_steps=24, progress_color='white', command=self.slider_command) # remember to change progress_color depending on value (red - green)
        self.len_slider.set(16) # set default value
        self.slider_command(16) # set the length variable
        self.save_button = ctk.CTkButton(     master=self.tab('Generate'), text='Save', width=70, height=30, corner_radius=10, command=self.save)
        # tab 1 placement
        self.password_result.grid( row=0,column=0, columnspan=3, padx=10,pady=20, sticky='ew')
        self.gen_button.grid(      row=1,column=0, columnspan=3, padx=10,pady=20)
        self.len_label.grid(       row=2,column=0,               padx=10,pady=15, sticky='e')
        self.len_slider.grid(      row=2,column=1,               padx=10,pady=15, sticky='w')
        self.save_button.grid(     row=2,column=2,               padx=10,pady=15)

        # vars for settings
        global lower_var, upper_var, numbers_var, symbols_var, punctuation_var, brackets_var
        upper_var = ctk.StringVar(value=True)
        lower_var = ctk.StringVar(value=True)
        numbers_var = ctk.StringVar(value=True)
        symbols_var = ctk.StringVar(value=True)
        punctuation_var = ctk.StringVar(value=True)
        brackets_var = ctk.StringVar(value=True)
        # tab 2 widgets
        self.check_lower = ctk.CTkCheckBox(       master=self.tab('Settings'), text='Letters (lower)', variable=lower_var)
        self.check_upper = ctk.CTkCheckBox(       master=self.tab('Settings'), text='Letters (upper)', variable=upper_var)
        self.check_numbers = ctk.CTkCheckBox(     master=self.tab('Settings'), text='Numbers', variable=numbers_var)
        self.check_symbols = ctk.CTkCheckBox(     master=self.tab('Settings'), text='Symbols', variable=symbols_var)
        self.check_punctuation = ctk.CTkCheckBox( master=self.tab('Settings'), text='Punctuation', variable=punctuation_var)
        self.check_brackets = ctk.CTkCheckBox(    master=self.tab('Settings'), text='Brackets', variable=brackets_var)
        #
        self.dark_switch = ctk.CTkSwitch(               master=self.tab('Settings'), text='Dark Mode', command=self.switch_var)
        self.button_color_label = ctk.CTkLabel(         master=self.tab('Settings'), text='Button color:')
        self.button_color_dropdown = ctk.CTkComboBox( master=self.tab('Settings'), values=['red','orange','yellow','green','blue','purple'], command=self.combo_command)
        # set all checkboxes by default (in order of suggestions bc i'm lazy)
        self.check_brackets.select()
        self.check_upper.select()
        self.check_lower.select()
        self.check_numbers.select()
        self.check_punctuation.select()
        self.check_symbols.select()
        # set dark mode switch depending on file
        if mode == 'dark':
            self.dark_switch.select()
        elif mode == 'light':
            self.dark_switch.deselect()
        # tab 2 placement
        self.check_upper.grid(       row=0,column=0, padx=10,pady=10, sticky='ew')
        self.check_lower.grid(       row=1,column=0, padx=10,pady=10, sticky='ew')
        self.check_numbers.grid(     row=2,column=0, padx=10,pady=10, sticky='ew')
        self.check_symbols.grid(     row=0,column=1, padx=10,pady=10, sticky='ew')
        self.check_punctuation.grid( row=1,column=1, padx=10,pady=10, sticky='ew')
        self.check_brackets.grid(    row=2,column=1, padx=10,pady=10, sticky='ew')
        #
        self.dark_switch.grid(       row=0,column=2, padx=20,pady=10, sticky='ew')
        self.button_color_label.grid(row=1,column=2, padx=20,pady=5,  sticky='sew')
        self.button_color_dropdown.grid(row=2,column=2, padx=20,pady=5, sticky='new')

# tab 1 functions
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

    def save(self):
        print('saved')

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
        

# tab 2 functions
    global lower_var, upper_var, numbers_var, symbols_var, punctuation_var, brackets_var

    def combo_command(self,choice):
        print(choice)
        def config(widget, text):
            widget.configure(fg_color=colour_dict[choice])
            widget.configure(hover_color=hover_dict[choice])
            if text:
                widget.configure(text_color=text_dict[choice])
        
        config(self.gen_button,        True)
        config(self.save_button,       True)
        config(self.check_brackets,    False)
        config(self.check_upper,       False)
        config(self.check_lower,       False)
        config(self.check_numbers,     False)
        config(self.check_punctuation, False)
        config(self.check_symbols,     False)
        

    def switch_var(self):
        global mode
        value = self.dark_switch.get()
        settings_path = writable_path('settings.txt')  #
        with open(settings_path, 'r') as file:         # file setup
            content = file.read()                      #
            if value == 1:
                ctk.set_appearance_mode('dark')
                mode = 'dark'
                with open (settings_path, 'w') as file:
                    file.write(content.replace('light','dark'))
            elif value == 0:
                ctk.set_appearance_mode('light')
                mode = 'light'
                with open (settings_path, 'w') as file:
                    file.write(content.replace('dark','light'))



class App (ctk.CTk):
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

app = App()
app.mainloop()
os._exit(0)