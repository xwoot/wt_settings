from PyQt5 import QtCore, QtGui, QtWidgets
import commentjson, re, random, os, matplotlib.font_manager
from shutil import copyfile

###############################################################################################

# Place dans le répertoire de "settings.json"
homePath = os.getenv("HOMEPATH")

if os.path.isdir(f"C:{homePath}\\LocalAppData\\Packages\\Microsoft.WindowsTerminal_8wekyb3d8bbwe\\LocalState"):
    os.chdir(f"C:{homePath}\\LocalAppData\\Packages\\Microsoft.WindowsTerminal_8wekyb3d8bbwe\\LocalState")
    settingsPath = f"C:{homePath}\\LocalAppData\\Packages\\Microsoft.WindowsTerminal_8wekyb3d8bbwe\\LocalState"
else:
    os.chdir(f"C:{homePath}\\AppData\\Local\\Packages\\Microsoft.WindowsTerminal_8wekyb3d8bbwe\\LocalState")
    settingsPath = f"C:{homePath}\\AppData\\Local\\Packages\\Microsoft.WindowsTerminal_8wekyb3d8bbwe\\LocalState"

# Crée une sauvegarde de "settings.json"
if not os.path.isfile(f"{settingsPath}\\settings.json.bak"):
    copyfile(f"{settingsPath}\\settings.json", f"{settingsPath}\\settings.json.bak")

    
# Ouvre "settings.son" et le charge en tant qu'objet
with open("settings.json", "r") as file:
    wt_schemes = file.read()
file.close()
data_schemes = commentjson.loads(wt_schemes)

# Ajoute les thèmes à "settings.json"
if len(data_schemes["schemes"]) <= 10:
    with open("windows-terminal-themes.json", "r") as file:
        wt_data = file.read()
    file.close()
    data_wt = commentjson.loads(wt_data)

    for i in data_wt:
        data_schemes["schemes"].append(i)

    with open("settings.json", "w") as file:
        commentjson.dump(data_schemes, file, indent=2)
    file.close()


# Écrit les modifications dans "settings.json"
def dumpJson():
    with open("settings.json", "w") as file:
        commentjson.dump(data_schemes, file, indent=2)
    file.close()

# Trouve le nom du profil par défaut
default_guid = data_schemes["defaultProfile"]

def findDefault():
    for item in data_schemes['profiles']['list']:
        if item['guid'] == default_guid:
            return item['name']
default_profile = findDefault()

# Crée la liste des thèmes
data_list = []
for item in data_schemes['schemes']:
    data_list.append(item['name'])

# Crée la liste des profils
profiles_list = []
for item in data_schemes['profiles']['list']:
    profiles_list.append(item['name'])

#Crée la liste des polices
fonts = matplotlib.font_manager.fontManager.ttflist
font_list = []
for f in fonts:
    font_list.append(f.name)
font_list = list(dict.fromkeys(sorted(font_list, key=str.lower)))

###############################################################################################



class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Windows Terminal Settings")
        MainWindow.setFixedSize(405, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)



        font = QtGui.QFont()
        font.setPointSize(10)

        self.schemeLabel = QtWidgets.QLabel(self.centralwidget)
        self.schemeLabel.setGeometry(QtCore.QRect(175, 25, 121, 31))
        self.schemeLabel.setFont(font)
        self.schemeLabel.setObjectName("Thème")
        self.schemeLabel.setText("Thème :")
        
        self.backgroundLabel = QtWidgets.QLabel(self.centralwidget)
        self.backgroundLabel.setGeometry(QtCore.QRect(175, 90, 125, 31))
        self.backgroundLabel.setFont(font)
        self.backgroundLabel.setObjectName("backgroundLabel")
        self.backgroundLabel.setText("Image d'arrière plan :")

        self.fontLabel = QtWidgets.QLabel(self.centralwidget)
        self.fontLabel.setGeometry(QtCore.QRect(175, 215, 125, 31))
        self.fontLabel.setFont(font)
        self.fontLabel.setObjectName("fontLabel")
        self.fontLabel.setText("Police :")

        self.opacityLabel = QtWidgets.QLabel(self.centralwidget)
        self.opacityLabel.setGeometry(QtCore.QRect(175, 155, 125, 31))
        self.opacityLabel.setFont(font)
        self.opacityLabel.setObjectName("opacityLabel")
        self.opacityLabel.setText("Opacité :")

        self.defaultButton = QtWidgets.QPushButton(self.centralwidget)
        self.defaultButton.setGeometry(QtCore.QRect(170, 330, 211, 36))
        self.defaultButton.setFont(font)
        self.defaultButton.setObjectName("pushButton")
        self.defaultButton.clicked.connect(self.changeDefault)

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(175, 288, 121, 31))
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.fontSize = QtWidgets.QSpinBox(self.centralwidget)
        self.fontSize.setGeometry(QtCore.QRect(290, 294, 42, 22))
        self.fontSize.setObjectName("spinBox")
        self.fontSize.valueChanged[int].connect(self.changeFontSize)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(175, 120, 200, 30))
        self.pushButton.setObjectName("Open File")
        self.pushButton.clicked.connect(self.changeBackgroundImage)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.fontBox = QtWidgets.QComboBox(self.centralwidget)
        self.fontBox.setGeometry(QtCore.QRect(175, 245, 200, 30))
        self.fontBox.setObjectName("fontBox")
        self.fontBox.activated[int].connect(self.changeFont)

        for item in font_list:
            self.fontBox.addItem(item)
        
        # index_fontBox = self.fontBox.findText(default_font, QtCore.Qt.MatchFixedString)
        # self.fontBox.setCurrentIndex(index_fontBox)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(175, 55, 200, 30))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.activated[int].connect(self.changeScheme)

        for item in data_list:
            self.comboBox.addItem(item)

        # index = self.comboBox.findText(default_scheme, QtCore.Qt.MatchFixedString)
        # self.comboBox.setCurrentIndex(index)

        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(175, 190, 160, 20))
        self.horizontalSlider.setMaximum(10)
        self.horizontalSlider.setSingleStep(1)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalSlider.sliderReleased.connect(self.changeOpacity)


        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(25, 25, 121, 350))
        self.listWidget.setObjectName("listWidget")
        
        for item in profiles_list:
            self.listWidget.addItem(item)
        
        self.listWidget.currentItemChanged.connect(self.changedProfile)
        index_listWidget = self.listWidget.findItems(default_profile, QtCore.Qt.MatchFixedString)
        self.listWidget.setCurrentRow(self.listWidget.row(index_listWidget[0]))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Paramètres"))
        self.pushButton.setText(_translate("MainWindow", "Choisir"))
        self.label.setText(_translate("MainWindow", "Taille de la police :"))
        self.defaultButton.setText(_translate("MainWindow", "Choisir comme profil par défaut"))
    
    # Retourne l'index du profil actuellement sélectionné
    def getCurrentIndex(self):
        currentProfile = self.listWidget.currentItem().text()
        for i, dic in enumerate(data_schemes['profiles']['list']):
            if dic["name"] == currentProfile:
                return i

    # Change le profil par défaut
    def changeDefault(self):
        currentProfile = self.listWidget.currentItem().text()
        for item in data_schemes['profiles']['list']:
            if item['name'] == currentProfile:
                data_schemes['defaultProfile'] = item['guid']
                dumpJson()

    # Change le thème
    def changeScheme(self, param):
        currentProfileIndex = self.getCurrentIndex()
        self.comboBox.setCurrentIndex(param)
        data_schemes["profiles"]['list'][currentProfileIndex]['colorScheme'] = self.comboBox.itemText(param)
        dumpJson()

    # Change la taille de la police
    def changeFontSize(self, param):
        currentProfileIndex = self.getCurrentIndex()
        data_schemes['profiles']['list'][currentProfileIndex]['fontSize'] = param
        dumpJson()
        
    # Change la police
    def changeFont(self, param):
        currentProfileIndex = self.getCurrentIndex()
        self.fontBox.setCurrentIndex(param)
        data_schemes['profiles']['list'][currentProfileIndex]['fontFace'] = self.fontBox.itemText(param)
        dumpJson()

    # Change l'opacité de l'image d'arrière-plan
    def changeOpacity(self):
        currentProfileIndex = self.getCurrentIndex()
        sliderValue = self.horizontalSlider.value()
        data_schemes["profiles"]["list"][currentProfileIndex]["backgroundImageOpacity"] = sliderValue / 10
        dumpJson()

    # Change l'image d'arrière plan
    def changeBackgroundImage(self):
        currentProfileIndex = self.getCurrentIndex()
        getFile = QtWidgets.QFileDialog.getOpenFileName(None, 'Open File')
        filename = getFile[0]
        filename = filename.replace(r"/","\\")
        data_schemes['profiles']['list'][currentProfileIndex]['backgroundImage'] = filename
        dumpJson()

    # Change de profil    
    def changedProfile(self):
        # currentProfile = self.listWidget.currentItem().text()
        currentProfileIndex = self.getCurrentIndex()
        
        if not "fontSize" in data_schemes['profiles']['list'][currentProfileIndex]:
            data_schemes['profiles']['list'][currentProfileIndex]['fontSize'] = "12"

        if not "fontFace" in data_schemes['profiles']['list'][currentProfileIndex]:
            data_schemes['profiles']['list'][currentProfileIndex]['fontFace'] = "Cascadia Code PL"
        
        if not "backgroundImageOpacity" in data_schemes['profiles']['list'][currentProfileIndex]:
            data_schemes['profiles']['list'][currentProfileIndex]['backgroundImageOpacity'] = 1.0
        
        if not "colorScheme" in data_schemes['profiles']['list'][currentProfileIndex]:
            data_schemes['profiles']['list'][currentProfileIndex]['colorScheme'] = "Atom"

        index = self.comboBox.findText(data_schemes['profiles']['list'][currentProfileIndex]['colorScheme'], QtCore.Qt.MatchFixedString)
        self.comboBox.setCurrentIndex(index)
        self.fontSize.setValue(int(data_schemes['profiles']['list'][currentProfileIndex]['fontSize']))
        index_fontBox = self.fontBox.findText(data_schemes['profiles']['list'][currentProfileIndex]['fontFace'], QtCore.Qt.MatchFixedString)
        self.fontBox.setCurrentIndex(index_fontBox)
        sliderValue = int(data_schemes['profiles']['list'][currentProfileIndex]['backgroundImageOpacity'] * 10) 
        self.horizontalSlider.setValue(sliderValue)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    app.setStyle('Fusion')
    app.setWindowIcon(QtGui.QIcon('Windows_Terminal_Logo_256x256.png'))
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
