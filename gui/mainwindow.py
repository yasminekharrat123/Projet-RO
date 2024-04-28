from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget,
                             QTableWidgetItem, QHBoxLayout, QHeaderView, QMainWindow)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Optimization Application")
        self.setGeometry(100, 100, 800, 400)
        self.setStyleSheet(
            "background-color: #333; color: #FFF; font-size: 16px;")

        self.central_widget = QWidget()
        self.central_widget.setStyleSheet("background-color: #555;")
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()

        self.choose_label = QLabel("Choose a model to run:")
        self.choose_label.setStyleSheet("font-weight: bold; padding: 10px;")
        layout.addWidget(self.choose_label)

        self.btn_transport = QPushButton("Transport Model")
        self.btn_transport.setStyleSheet("QPushButton { background-color: #5F85DB; color: #FFF; padding: 10px; margin: 10px; }"
                                         "QPushButton:hover { background-color: #5078C8; }")
        self.btn_crew = QPushButton("Crew Scheduling Model")
        self.btn_crew.setStyleSheet("QPushButton { background-color: #5F85DB; color: #FFF; padding: 10px; margin: 10px; }"
                                    "QPushButton:hover { background-color: #5078C8; }")
        self.btn_transport.clicked.connect(self.open_transport_model)
        self.btn_crew.clicked.connect(self.open_crew_model)

        layout.addWidget(self.btn_transport)
        layout.addWidget(self.btn_crew)

        self.central_widget.setLayout(layout)

    def open_transport_model(self):
        self.model_form = TransportForm()
        self.model_form.show()

    def open_crew_model(self):
        self.model_form = CrewForm()
        self.model_form.show()


class BaseForm(QWidget):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #444; color: #EEE;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.table = QTableWidget()
        self.table.setStyleSheet("QTableWidget { background-color: #FFF; color: #333; }"
                                 "QHeaderView::section { background-color: #666; color: #FFF; padding: 5px; }")
        self.layout.addWidget(self.table)

        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.setStyleSheet(
            "background-color: #5FA8DB; color: #FFF; padding: 10px; margin: 10px;")
        self.add_row_button.clicked.connect(self.add_row)
        self.layout.addWidget(self.add_row_button)

        self.submit_button = QPushButton("Submit")
        self.submit_button.setStyleSheet(
            "background-color: #5DBB89; color: #FFF; padding: 10px; margin: 10px;")
        self.submit_button.clicked.connect(self.submit)
        self.layout.addWidget(self.submit_button)


class TransportForm(BaseForm):
    def __init__(self):
        super().__init__("Transport Model Inputs")
        self.init_ui()

    def init_ui(self):
        # Initialize table with headers
        self.table.setColumnCount(7)  # Include 'Supply' in columns
        self.table.setHorizontalHeaderLabels(
            ["Origin", "Destination", "Mode", "Capacity", "Cost", "Demand", "Supply"])
        self.add_initial_rows()

    def add_initial_rows(self):
        for _ in range(3):  # Adding 3 initial rows
            self.add_row()

    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        for i in range(7):  # 7 columns to fill
            self.table.setItem(row_position, i, QTableWidgetItem(""))

    def submit(self):
        origins = set()
        destinations = set()
        modes = set()
        costs = {}
        capacities = {}
        demand = {}
        supply = {}

        for row in range(self.table.rowCount()):
            origin = self.table.item(row, 0).text()
            destination = self.table.item(row, 1).text()
            mode = self.table.item(row, 2).text()
            capacity = self.table.item(row, 3).text()
            cost = self.table.item(row, 4).text()
            dem = self.table.item(row, 5).text()
            sup = self.table.item(row, 6).text()

            origins.add(origin)
            destinations.add(destination)
            modes.add(mode)

            costs[(origin, destination, mode)] = float(cost) if cost else 0
            capacities[(origin, destination, mode)] = float(
                capacity) if capacity else 0
            if destination not in demand or float(dem) > demand[destination]:
                demand[destination] = float(dem) if dem else 0
            if origin not in supply or float(sup) > supply[origin]:
                supply[origin] = float(sup) if sup else 0

        # Now call the model function with these organized inputs
        from model.transport import run_transport_model
        run_transport_model(list(origins), list(destinations), list(
            modes), capacities, costs, demand, supply)
        print("Data submitted. Model should now run with the provided inputs.")


class CrewForm(BaseForm):
    def __init__(self):
        super().__init__("Crew Scheduling Model Inputs")
        self.init_ui()

    def init_ui(self):
        # Initialize table with headers
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["Crew Name", "Flight", "Qualified (Yes/No)", "Cost"])
        self.add_initial_rows()

    def add_initial_rows(self):
        for _ in range(2):  # Adding 2 initial rows
            self.add_row()

    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(""))  # Crew Name
        self.table.setItem(row_position, 1, QTableWidgetItem(""))  # Flight
        # Checkbox for qualification
        chkBoxItem = QTableWidgetItem()
        chkBoxItem.setFlags(chkBoxItem.flags() | Qt.ItemIsUserCheckable)
        chkBoxItem.setCheckState(Qt.Unchecked)
        self.table.setItem(row_position, 2, chkBoxItem)
        self.table.setItem(row_position, 3, QTableWidgetItem(""))  # Cost

    def submit(self):
        crew = []
        flights = []
        qualifications = {}
        costs = {}

        for row in range(self.table.rowCount()):
            crew_name = self.table.item(row, 0).text()
            flight = self.table.item(row, 1).text()
            qualified = self.table.item(row, 2).checkState() == Qt.Checked
            cost = float(self.table.item(row, 3).text()
                         ) if self.table.item(row, 3).text() else 0

            crew.append(crew_name)
            if flight not in flights:
                flights.append(flight)

            qualifications[(crew_name, flight)] = qualified
            costs[(crew_name, flight)] = cost

        print("Collected data from Crew Form:",
              crew, flights, qualifications, costs)
        from model.crew import run_crew_scheduling_model
        run_crew_scheduling_model(crew, flights, qualifications, costs)
