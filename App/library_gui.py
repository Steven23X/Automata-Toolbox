import customtkinter
import sys
import os
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1100x600")
        self.resizable(False,False)
        self.title("Automaton")
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("dark-blue") 
        self.input_frame=customtkinter.CTkFrame(self)
        self.label_input=customtkinter.CTkLabel(self.input_frame,text="INPUT:",corner_radius=8,font=('Times New Roman',17,'bold'))
        self.input_text=customtkinter.CTkTextbox(self,width=400,height=500,font=('Times New Roman',17,'bold'))
        self.output_frame=customtkinter.CTkFrame(self)
        self.label_output=customtkinter.CTkLabel(self.output_frame,text="OUTPUT:",corner_radius=8,font=('Times New Roman',17,'bold'))
        self.output_text=customtkinter.CTkTextbox(self,width=400,height=500,font=('Times New Roman',17,'bold'))
        self.output_text.configure(state="disabled")
        self.f1=customtkinter.CTkFrame(self)
        self.test_button = customtkinter.CTkButton(self.f1, text="FA VALIDATOR",command=self.runfavalidator,font=('Times New Roman',17,'bold'))
        self.clear_button = customtkinter.CTkButton(self.f1, text="CLEAR ALL",command=self.clearall,font=('Times New Roman',17,'bold'))
        self.openfile_button = customtkinter.CTkButton(self.f1, text="FILE SAMPLE",command=self.filesample,font=('Times New Roman',17,'bold'))
        self.input_frame.grid(row=0,column=0,padx=20,pady=10)
        self.input_text.grid(row=1,column=0,padx=20,pady=10)
        self.f1.grid(row=1,column=2,padx=20,pady=10)
        self.output_frame.grid(row=0,column=3,padx=20,pady=10)
        self.output_text.grid(row=1,column=3,padx=20,pady=10)
        self.openfile_button.pack(side=customtkinter.TOP,padx=20,pady=10)
        self.test_button.pack(side=customtkinter.TOP,padx=20,pady=10)
        self.clear_button.pack(side=customtkinter.TOP,padx=20,pady=10)
        self.label_input.pack()
        self.label_output.pack()

        sys.stdout.write=self.redirector
    
    def filesample(self):
        text_file = open(os.path.abspath('Files/sample.txt'), "r")
        content = text_file.read()
        self.input_text.delete("1.0","end")
        self.input_text.insert(customtkinter.END, content)
        text_file.close()

    def runfavalidator(self):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0","end")
        text_file = open(os.path.abspath('Files/input.txt'), "w")
        text_file.write(self.input_text.get(1.0, customtkinter.END))
        text_file.close()
        exec(open(os.path.abspath('Validators/FAValidator/fa.py')).read())
        self.output_text.configure(state="disabled")

    def clearall(self):
        self.output_text.configure(state="normal")
        self.input_text.delete("1.0","end")
        self.output_text.delete("1.0","end")
        self.output_text.configure(state="disabled")

    def redirector(self,inputStr):
        self.output_text.insert(customtkinter.INSERT, inputStr)
