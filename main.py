import sys, json, os
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QComboBox, QPushButton, QLabel, QHBoxLayout,QVBoxLayout, QBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from googletrans import Translator

# 

class Main(QWidget):

    # Creat the variable that will display my profit
    globalProfit = ""

    def __init__(self):
        super().__init__()
        self.settings()
        self.rememberProfit()
        self.initUI()
        self.button_function()
        

    #create UI 
    def initUI(self):
        # Text Input
        self.input_box = QTextEdit()

        # Profit Number
        self.profit_num = QLabel(Main.globalProfit)
        self.profit_num.setAlignment(Qt.AlignCenter)
        self.profit_num.setFont(QFont("Arial", 60))

        #Buttons
        self.button_row = QHBoxLayout()

        self.add_button = QPushButton()
        self.add_button.setProperty("cssClass", "green_text")
        self.add_button.setText("Gain")
        self.add_button.setObjectName("Gain")


        self.sub_button = QPushButton()
        self.sub_button.setProperty("cssClass", "red_text")
        self.sub_button.setText("Loss")
        self.sub_button.setObjectName("Loss")

        self.button_row.addWidget(self.add_button, 50)
        self.button_row.addWidget(self.sub_button, 50)

        #Final Layout
        self.master = QVBoxLayout()
        self.master.addWidget(self.profit_num, 50)
        self.master.addLayout(self.button_row, 30)
        self.master.addWidget(self.input_box, 20)

        self.setLayout(self.master)

        self.setStyleSheet("""
                QLabel {
                    color: #2E8B57;
                }
                
                QPushButton#Gain {
                    color: #2E8B57;
                }
                           
                QPushButton#Loss {
                    color: #9B111E;
                }
                           
                Main {
                    background-color: #050301;    
                }
            """
        )


    #create window settings
    def settings(self):
        self.setWindowTitle("Profit Tracker")
        self.setGeometry(250,250,600,500)

    #create button function
    def button_function(self):
        self.add_button.clicked.connect(self.addition)
        self.sub_button.clicked.connect(self.subtraction)
        

    #add function
    def addition(self):
        #Collect input
        num_str = self.input_box.toPlainText()
        num = float(num_str)

        #Collect current profit value
        num_str2 = self.profit_num.text()
        num_str2 = num_str2[1:len(num_str2)]
        num2 = float(num_str2)

        #Find final profit sum & set it as new profit
        sum = round(num + num2, 2)
        self.writeToJson("total", str(sum), "storage.json")
        self.profit_num.setText("$" + str(sum))

        #Clear input_box
        self.input_box.clear()

    #subtract function
    def subtraction(self):
        #Collect input
        num_str = self.input_box.toPlainText()
        num = float(num_str)

        #Collect current profit value
        num_str2 = self.profit_num.text()
        num_str2 = num_str2[1:len(num_str2)]
        num2 = float(num_str2)

        #Find final profit sum & set it as new profit
        sum = round(num2 - num, 2)
        self.writeToJson("total", str(sum), "storage.json")
        self.profit_num.setText("$" + str(sum))

        #Clear input_box
        self.input_box.clear()

    # Function to write to my JSON file, made to store the profit number
    def writeToJson(self, keyName, toStore, filePath):
        #stole from online, try catch statement that works to make sure the filepath entered is valid
        try:
            with open(filePath, 'r') as jsonfile:
                data = json.load(jsonfile)
        except FileNotFoundError:
            print(f"Error: The file {filePath} was not found.")
            exit()
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from the file {filePath}.")
            exit()    

        #assign new value to key
        data[keyName] = toStore

        #replace json file
        with open(filePath, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)
    
    # Function to read my JSON file, made to collect the profit number from memory on launch
    def readFromJson(self, keyName, filePath):
        #stole from online, try catch statement that works to make sure the filepath entered is valid
        try:
            with open(filePath, 'r') as jsonfile:
                data = json.load(jsonfile)
            
                value = data.get(keyName)
            
                if value is not None:
                    return value #returns the vlaue I want to read
                else:
                    return f"Key '{keyName}' not found in the JSON file."
        except FileNotFoundError:
            return f"Error: The file '{jsonfile}' was not found."
        except json.JSONDecodeError:
            return f"Error: Could not decode JSON from the file '{jsonfile}'."
    
    # Recall profit from json
    def rememberProfit(self):
        self.displayedProfit = "$" + str(self.readFromJson("total", "storage.json"))
        Main.globalProfit = self.displayedProfit

#Launch window
if __name__ in "__main__":
    app = QApplication([])
    main = Main()
    main.show()
    sys.exit(app.exec_())