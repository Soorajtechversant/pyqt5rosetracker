from PyQt5.QtCore import QTime, QTimer
from PyQt5.QtWidgets import QApplication, QTimeEdit

# Create a new application instance
app = QApplication([])

# Create a new QTimeEdit widget
time_edit = QTimeEdit()

# Set the time to the current time
current_time = QTime.currentTime()
time_edit.setTime(current_time)

# Update the time every second using a QTimer
timer = QTimer()
timer.timeout.connect(lambda: time_edit.setTime(QTime.currentTime()))
timer.start(1000)

# Show the widget
time_edit.show()

# Run the application
app.exec_()




# In this code snippet, we create a new QTimeEdit widget 
# and set its time to the current time using QTime.currentTime() and setTime().
# We then create a QTimer that updates the time every second by 
# calling QTime.currentTime() and setting the time in the QTimeEdit
# widget using setTime(). Finally, we show the widget and 
# start the application event loop with app.exec_().