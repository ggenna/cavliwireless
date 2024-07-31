# ComPort class used in Qt terminal programs

from PySide6.QtCore import QIODevice, Qt, Slot, QTimer
from PySide6.QtSerialPort import QSerialPort
from PySide6.QtWidgets import QPushButton, QComboBox, QGridLayout, QLineEdit, QLabel, QGroupBox
from serial.tools import list_ports

class ComPort(QGroupBox):  # QWidget
    def __init__(self, name='', baud_rate='115200', flow_control='NO'):
        super().__init__()
        self.setTitle('Serial port ' + name)
        self.setStyleSheet("background-color: white;")
        # add layout
        layout = QGridLayout(self)
        # baud rates
        self.b_rates = ['9600', '14400', '19200', '28800', '33600', '38400', '57600', '115200', '230400', '460800',
                        '921600']
        
        self.flowc = ['NO', 'SW ctrl flow', 'HW ctrl flow']
        self.nmax = 300  # max number of COM port
        self.port_timeout = 0.5  # COM port timeout
        # create buttons, etc
        self.info_label = QLabel('COM closed')
        self.info_label.setStyleSheet('color: red;')
        self.info_label.setMinimumWidth(10)
        self.info_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.info_label, 0, 0)
        #
        self.port_number_label = QLabel('Port number: ')
        self.port_number_label.setStyleSheet('color: #555555;')
        self.port_number_label.setMinimumWidth(10)
        self.port_number_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.port_number_label, 0, 2)
        #
        
        
        # self.port_field = QLineEdit()
        # self.port_field.setAlignment(Qt.AlignCenter)
        # layout.addWidget(self.port_field, 0, 2)

        self.com_ports_combobox = QComboBox(self)
        self.com_ports_combobox.setMaximumWidth(65)
        layout.addWidget(self.com_ports_combobox, 0, 3)
       
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_com_ports)
        self.timer.start(5000)  # Aggiorna ogni 5000 millisecondi (5 secondi)

        #
        self.open_btn = QPushButton('Open')
        self.open_btn.setStyleSheet('background-color: #00dd00;')
        layout.addWidget(self.open_btn, 0, 4)
        self.open_btn.clicked.connect(self.open_port)


        ###
        self.flowcontrol_label = QLabel('Flow control: ')
        self.flowcontrol_label.setStyleSheet('color: #555555;')
        self.flowcontrol_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.flowcontrol_label, 1, 0)
        #
        self.flowcontrol = QComboBox()
        self.flowcontrol.addItems(self.flowc)

        if self.flowc.count(flow_control):
            self.flowcontrol.setCurrentIndex(self.flowc.index(flow_control))  # set default item
        self.flowcontrol.setMaximumWidth(75)
        layout.addWidget(self.flowcontrol, 1, 1)

        ###
        self.baud_rate_label = QLabel('Baud rate: ')
        self.baud_rate_label.setStyleSheet('color: #555555;')
        self.baud_rate_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.baud_rate_label, 1, 2)
        #
        self.baud_rates = QComboBox()
        self.baud_rates.addItems(self.b_rates)
        if self.b_rates.count(baud_rate):
            self.baud_rates.setCurrentIndex(self.b_rates.index(baud_rate))  # set default item
        layout.addWidget(self.baud_rates, 1, 3)
        #
        self.close_btn = QPushButton('Close')
        self.close_btn.setStyleSheet('background-color: red;')
        layout.addWidget(self.close_btn, 1, 4)
        self.close_btn.clicked.connect(self.close_port)
        # serial port
        self.com_opened = 0
        # self.baud_rate = int(baud_rate)
        self.ser = QSerialPort()
        self.ser.errorOccurred.connect(self.ser_error)

    
    def update_com_ports(self):
        com_ports = [port.device for port in list_ports.comports()]
        self.com_ports_combobox.clear()
        self.com_ports_combobox.addItems(com_ports)

    def open_port(self):
        n = 0
        self.timer.stop()
        self.port_field = self.com_ports_combobox.currentText()
        print(f"Porta COM selezionata: {self.com_ports_combobox.currentText()}")
   
        if self.com_opened == 0:
            com_num = self.port_field
            br = self.baud_rates.currentText()
            self.ser.setBaudRate(int(br))
            if com_num:
                
                    self.ser.setPortName(com_num)
                    self.ser.open(QIODevice.ReadWrite)
                    if self.ser.isOpen():
                        self.info_label.setText(com_num + ' opened')
                        self.info_label.setStyleSheet('color: #00dd00;')  # green
                        self.com_opened = 1
                    else:
                        self.info_label.setText(com_num+' is busy')
                        self.info_label.setStyleSheet('color: red;')
                        self.com_opened = 0        
            else:
                    self.info_label.setText('Can not open, reboot')
                    self.info_label.setStyleSheet('color: red;')

        

    def close_port(self):
        if self.com_opened:
            self.ser.close()
            self.info_label.setText('COM closed')
            self.info_label.setStyleSheet('color: red;')
            self.com_opened = 0

    @Slot()
    def ser_error(self):
        err = self.ser.error()
        if err == QSerialPort.SerialPortError.NoError:  # if error message is "No error"
            pass
        else:
            self.close_port()  # close port if some error occurred...

    def write(self, data):
        if self.com_opened:
            self.ser.write(data)