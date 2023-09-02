import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
import threading
import time
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MemoryMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Monitor")
        
        self.log_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, state=tk.DISABLED)
        self.log_widget.pack(padx=10, pady=10)
        
        self.threshold_label = tk.Label(root, text="Threshold (MB):")
        self.threshold_label.pack(pady=5)
        
        self.threshold_slider = ttk.Scale(root, from_=0, to=8000, length=200, orient="horizontal")
        self.threshold_slider.set(1000)
        self.threshold_slider.pack(pady=5)
        
        self.start_button = tk.Button(root, text="Start Monitoring", command=self.toggle_monitoring)
        self.start_button.pack(pady=5)
        
        # Live graph setup
        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        self.ax.set_xlabel("Time")
        self.ax.set_ylabel("Memory Usage (MB)")
        self.memory_data = []
        self.time_data = []
        self.line, = self.ax.plot(self.time_data, self.memory_data)
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack(padx=10, pady=10)
        
        self.monitoring = False
        self.monitoring_thread = None
        
    def monitor_memory(self):
        while self.monitoring:
            threshold = self.threshold_slider.get()
            memory_info = psutil.virtual_memory()
            memory_usage_mb = memory_info.used / (1024.0 ** 2)
            
            self.memory_data.append(memory_usage_mb)
            self.time_data.append(time.time())
            
            if len(self.memory_data) > 20:  # Limit the number of data points displayed
                self.memory_data.pop(0)
                self.time_data.pop(0)
            
            self.line.set_xdata(self.time_data)
            self.line.set_ydata(self.memory_data)
            self.ax.relim()
            self.ax.autoscale_view()
            
            if memory_usage_mb > threshold:
                self.log_widget.config(state=tk.NORMAL)
                self.log_widget.insert(tk.END, f"Memory usage is {memory_usage_mb:.2f} MB - Exceeded threshold of {threshold:.2f} MB!\n")
                self.log_widget.config(state=tk.DISABLED)
            
            self.canvas.draw()
            
            time.sleep(5)
    
    def toggle_monitoring(self):
        if self.monitoring:
            self.monitoring = False
            self.start_button.config(text="Start Monitoring")
            self.monitoring_thread.join()
            self.monitoring_thread = None
        else:
            self.monitoring = True
            self.start_button.config(text="Stop Monitoring")
            self.monitoring_thread = threading.Thread(target=self.monitor_memory)
            self.monitoring_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = MemoryMonitorApp(root)
    root.mainloop()
