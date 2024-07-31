# Controls for terminals

from PySide6.QtCore import Qt, QCoreApplication, QDate 
from PySide6.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QCheckBox, QLabel, QFileDialog
from PySide6.QtWidgets import QTabWidget, QTextEdit, QGridLayout, QButtonGroup, QLineEdit, QGroupBox
        

class Controls(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle('Controls')
        self.setStyleSheet("background-color: white;")
        # add layout
        layout = QGridLayout(self)
        # create buttons, etc
        self.time_box = QCheckBox('Add time', self)
        layout.addWidget(self.time_box, 0, 0)
        #
        self.echo_box = QCheckBox('Echo Tx', self)
        layout.addWidget(self.echo_box, 0, 1)
        #
        self.clear_btn = QPushButton('Clear term')
        self.clear_btn.setStyleSheet('background-color: #333333; color: #eeeeee;')
        layout.addWidget(self.clear_btn, 1, 0)
        #
        self.copy_btn = QPushButton('Copy from term')
        self.copy_btn.setStyleSheet('background-color: #999999;')
        layout.addWidget(self.copy_btn, 0, 2)
        #
        self.cut_btn = QPushButton('Cut from term')
        self.cut_btn.setStyleSheet('background-color: #999999;')
        layout.addWidget(self.cut_btn, 1, 2)
        #
        self.info_btn = QPushButton('Ports info')
        self.info_btn.setStyleSheet('background-color: #ffff00;')
        layout.addWidget(self.info_btn, 0, 3)
        #
        self.free_btn = QPushButton('Get free ports')
        self.free_btn.setStyleSheet('background-color: #ffff00;')
        layout.addWidget(self.free_btn, 1, 3)


class ControlsTCP(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle('Controls')
        self.setStyleSheet("background-color: white;")
        # add layout
        layout = QGridLayout(self)
        # Line 0
        # create clear_btn
        self.clear_btn = QPushButton('Clear term')
        self.clear_btn.setStyleSheet('background-color: #333333; color: #eeeeee;')
        layout.addWidget(self.clear_btn, 0, 0)


class SendAny(QWidget):
    def __init__(self):
        super().__init__()
        # add layout
        self.setStyleSheet("background-color: white;")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        #
        self.any_field = QLineEdit()
        self.any_field.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.any_field)
        #
        self.suca = QPushButton('Send')
        self.suca.setStyleSheet('background-color: #ffffff;')
        layout.addWidget(self.suca)


class NewButton(QPushButton):
    cmd = ''
   
    def __init__(self, lbl):
        super().__init__()
        self.setText(lbl)
        self.setMinimumHeight(20)

    def set_cmd(self, cmd):
        self.cmd = cmd

    def get_cmd(self):
        return self.cmd


class Notebook(QTabWidget):

    def_btn_fg_color = 'black'
    def_btn_bg_color = '#eeeeee'
    btn_font_family = 'Titillium'
    btn_font_size = '12px'

    def __init__(self):
        super().__init__()

    # method to add Tables with buttons
    def add_tab_btn(self, tab_name, btn_data, handler):
        # create new table
        tab = QWidget()
        self.addTab(tab, tab_name)
        layout = QGridLayout(tab)
        # add buttons' group
        group = QButtonGroup(self)
        group.buttonClicked.connect(handler)
        c = 0        # defines number of column of buttons in the grid
        for col in btn_data:
            i = 0        # counter to define number of line of the buttons in the grid
            for btn in col:
                if btn[0]:                         # if the button's label is not empty
                    b = NewButton(btn[0])          # create button object
                    b.set_cmd(btn[1])              # set button's command
                    group.addButton(b)
                    layout.addWidget(b, i, c)
                    if not btn[2]: btn[2] = self.def_btn_fg_color   # if foreground colour is not defined use default one
                    if not btn[3]: btn[3] = self.def_btn_bg_color   # if background colour is not defined use default one
                    b.setStyleSheet('background-color: ' + btn[3] + '; ' +
                                    'color: ' + btn[2] + '; ' +
                                    'font-family: ' + self.btn_font_family + '; ' +
                                    'font-size: ' + self.btn_font_size + ';')
                i = i + 1   # next line
            c = c + 1       # next column

    # method to add Tables with editable fields
    def add_tab_edit(self, tab_name, num_of_fields, tab_data, handler):
        at_commands_panel = QWidget(self)
        self.addTab(at_commands_panel, tab_name)
        
        at_commands_layout = QVBoxLayout(at_commands_panel)

        # Aggiunta di una nuova QCheckBox prima della lista
        new_checkbox = QCheckBox('Select ALL NL', at_commands_panel)
        at_commands_layout.addWidget(new_checkbox)

        ###################### Aggiunto pulsante per esportare i comandi ##########################################
  
        self.export_button = QPushButton('Esporta Comandi', self)
        at_commands_layout.addWidget(self.export_button)

        self.export_button.clicked.connect(self.export_commands)

        # Funzione per copiare lo stato di new_checkbox a tutte le checkbox "NL"
        def copy_new_checkbox_state():
            new_checkbox_state = new_checkbox.isChecked()
            for i in range(20):  # Ridotto da 30 a 20
                nl_checkbox = at_commands_panel.findChild(QCheckBox, f"nl_checkbox_{i}")
                if nl_checkbox:
                    nl_checkbox.setChecked(new_checkbox_state)

        new_checkbox.clicked.connect(copy_new_checkbox_state)

        # Lista per memorizzare gli oggetti QLineEdit
        self.command_inputs = []

        for i in range(20):  # Ridotto da 30 a 20
            command_layout = QHBoxLayout()

            command_label = QLabel(f'{i + 1}:', at_commands_panel)
            #command_input = QLineEdit(at_commands_panel)
           # command_input.setMaximumSize(command_input.maximumWidth() // 2, command_input.maximumHeight())  # Dimezza la dimensione
            hex_checkbox = QCheckBox('HEX', at_commands_panel)
            nl_checkbox = QCheckBox('NL', at_commands_panel)
            nl_checkbox.setObjectName(f"nl_checkbox_{i}")

            send_button = SendAny()
            send_button.suca.clicked.connect(handler)

            command_layout.addWidget(command_label)
            #command_layout.addWidget(command_input)
            command_layout.addWidget(send_button)
            command_layout.addWidget(hex_checkbox)
            command_layout.addWidget(nl_checkbox)
            


            
            at_commands_layout.addLayout(command_layout)

           
            # Aggiungi il QLineEdit alla lista
            self.command_inputs.append(send_button.any_field)


        



    """
        # create new table
        tab = QWidget()
        self.addTab(tab, tab_name)
        layout = QVBoxLayout(tab)
        numero = len(tab_data) 
        for each in range(numero):
            fld = SendAny()
            fld.any_btn.clicked.connect(handler)
            fld.any_btn.setStyleSheet('background-color: #FFB273')
            layout.addWidget(fld)
            try:
                fld.any_field.setText(tab_data[each])
            except Exception:
                pass
    """
    def export_commands(self):
            # Assicurati che le dimensioni dei widget siano aggiornate

            
            QCoreApplication.processEvents()

            # Recupera tutti i comandi dalle QLineEdit e li esporta in un file di testo
            commands_text = ""
           
            for i, command_input in enumerate(self.command_inputs):
                command_text = command_input.text()
                commands_text += f"{i + 1}: {command_text}\n"

            # Ottieni la data corrente e formattala come richiesto
            current_date = QDate.currentDate()
            formatted_date = current_date.toString("dd-MM-yyyy")

            # Costruisci il percorso completo del file
            file_path, _ = QFileDialog.getSaveFileName(self, 'Salva Comandi', f'Comandi_{formatted_date}.txt', 'File di testo (*.txt)')

            # Assicurati che le dimensioni dei widget siano aggiornate nuovamente prima di scrivere nel file
            QCoreApplication.processEvents()

            # Scrivi i comandi nel file di testo
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(commands_text)

class LogMonitor(QGroupBox):
    def __init__(self):
        super().__init__()
        self.setTitle('Log monitor')
        self.setStyleSheet("background-color: white;")
        # add layout
        layout = QVBoxLayout(self)
        # create log monitor
        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setStyleSheet("""
                        background-color: #101010;
                        color: #FFFFFF;
                        font-family: Ariel;
                        font-size: 11px;
                        """)
        layout.addWidget(self.log)
        # create clear_log_btn
        self.clear_log_btn = QPushButton('Clear log')
        self.clear_log_btn.setStyleSheet('background-color: #333333; color: #eeeeee;')
        self.clear_log_btn.clicked.connect(self.clear_log)
        layout.addWidget(self.clear_log_btn)

    def clear_log(self):
        self.log.clear()               # clear log monitor