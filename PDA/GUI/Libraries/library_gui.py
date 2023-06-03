import customtkinter
import sys
import os


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # window attributes
        self.geometry("1110x600")
        self.resizable(False, False)
        self.title("Automaton")
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue")

        # left frame (input)
        self.input_frame = customtkinter.CTkFrame(self)
        self.label_input1 = customtkinter.CTkLabel(
            self.input_frame, text="INPUT:", corner_radius=8, font=('Times New Roman', 17, 'bold'))
        self.input_text = customtkinter.CTkTextbox(
            self.input_frame, width=400, height=400, font=('Times New Roman', 17, 'bold'))
        self.label_input2 = customtkinter.CTkLabel(
            self.input_frame, text="INPUT STRING:", corner_radius=8, font=('Times New Roman', 17, 'bold'))
        self.input_string = customtkinter.CTkTextbox(
            self.input_frame, width=400, height=100, font=('Times New Roman', 17, 'bold'))

        # right frame (output)
        self.output_frame = customtkinter.CTkFrame(self)
        self.label_output = customtkinter.CTkLabel(
            self.output_frame, text="OUTPUT:", corner_radius=8, font=('Times New Roman', 17, 'bold'))
        self.output_text = customtkinter.CTkTextbox(
            self.output_frame, width=400, height=525, font=('Times New Roman', 17, 'bold'))
        self.output_text.configure(state="disabled")

        # middle frame (buttons)
        self.f1 = customtkinter.CTkFrame(self)
        self.test_button1 = customtkinter.CTkButton(
            self.f1, text="PDA VALIDATOR", command=self.runpdavalidator, font=('Times New Roman', 17, 'bold'))
        self.clear_button = customtkinter.CTkButton(
            self.f1, text="CLEAR ALL", command=self.clearall, font=('Times New Roman', 17, 'bold'))
        self.openfile_button = customtkinter.CTkButton(
            self.f1, text="FILE SAMPLE", command=self.filesample, font=('Times New Roman', 17, 'bold'))

        # putting frames on grid
        self.input_frame.grid(row=0, column=0, padx=20, pady=10)
        self.f1.grid(row=0, column=1, padx=20, pady=10)
        self.output_frame.grid(row=0, column=2, padx=20, pady=10)
        self.openfile_button.pack(side=customtkinter.TOP, padx=20, pady=10)

        # packing items
        self.test_button1.pack(side=customtkinter.TOP, padx=20, pady=10)
        self.clear_button.pack(side=customtkinter.TOP, padx=20, pady=10)
        self.label_input1.pack()
        self.input_text.pack()
        self.label_input2.pack()
        self.input_string.pack()
        self.label_output.pack()
        self.output_text.pack()

        sys.stdout.write = self.redirector

    def filesample(self):
        """
        filesample inserts sample.txt into input_text
        """
        text_file = open(os.path.abspath('Files/sample.txt'), "r")
        content = text_file.read()
        self.input_text.delete("1.0", "end")
        self.input_text.insert(customtkinter.END, content)
        text_file.close()

    def clearall(self):
        """
        clearall is a command for the ClearAll button
        that deletes the input_text,output_text and input_string
        """
        self.output_text.configure(state="normal")
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.input_string.delete("1.0", "end")
        self.output_text.configure(state="disabled")

    def redirector(self, inputStr):
        """
        redirector changes the stdout -> output_text
        """
        self.output_text.insert(customtkinter.INSERT, inputStr)

    def runpdavalidator(self):
        """
        runpdavalidator runs pda_validator.py
        """
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", "end")
        text_file = open(os.path.abspath('Files/input.txt'), "w")
        text_file.write(self.input_text.get(1.0, customtkinter.END))
        text_file.close()
        text_file = open(os.path.abspath('Files/string.txt'), "w")
        text_file.write(self.input_string.get(1.0, customtkinter.END))
        text_file.close()
        exec(open(os.path.abspath('pda_validator.py')).read())
        self.output_text.configure(state="disabled")
