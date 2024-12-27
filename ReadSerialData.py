import serial
import matplotlib.pyplot as plt
import numpy as np
import time

# Konfigurasi serial
arduino_port = 'COM4'  # Ganti dengan port Arduino Anda
baud_rate = 115200     # Kecepatan baud yang sesuai
max_data_points = 200  # Jumlah data maksimum yang ditampilkan di plot

# Membuka koneksi serial
try:
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    time.sleep(2)  # Tunggu hingga koneksi stabil
    print("Koneksi serial berhasil dibuka.")
except serial.SerialException as e:
    print(f"Kesalahan membuka port serial: {e}")
    exit()

# Inisialisasi data
x_data = []  # Data untuk akselerometer X
adc_data = []  # Data untuk nilai ADC

# Setup plotting
plt.ion()
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))

# Plot akselerometer X
line1, = ax1.plot([], [], label='Accelerometer X (g)', color='b')
ax1.set_xlim(0, max_data_points)
ax1.set_ylim(-2, 2)
ax1.set_xlabel('Data Points')
ax1.set_ylabel('Acceleration (g)')
ax1.legend()
ax1.set_title("Real-Time Accelerometer Data")

# Plot ADC
line2, = ax2.plot([], [], label='ADC Voltage', color='r')
ax2.set_xlim(0, max_data_points)
ax2.set_ylim(0, 3.3)  # Rentang tegangan ADC (0 - 3.3V)
ax2.set_xlabel('Data Points')
ax2.set_ylabel('Voltage (V)')
ax2.legend()
ax2.set_title("Real-Time ADC Data")

# Loop utama
try:
    while True:
        if ser.in_waiting > 0:  # Cek apakah ada data di serial buffer
            raw_line = ser.readline().decode('utf-8').strip()  # Membaca data
            print(f"Data diterima: {raw_line}")  # Debugging

            # Memisahkan dan memproses data
            if ',' in raw_line and raw_line.count(',') == 1:
                try:
                    ax_g, adc_value = raw_line.split(',')
                    ax_g = float(ax_g)  # Konversi akselerasi ke float
                    adc_value = int(adc_value)  # Konversi ADC ke integer
                    voltage = (adc_value / 4095.0) * 3.3  # Konversi ADC ke tegangan

                    # Tambahkan data baru ke list
                    x_data.append(ax_g)
                    adc_data.append(voltage)

                    # Pastikan data tidak melebihi max_data_points
                    if len(x_data) > max_data_points:
                        x_data.pop(0)
                    if len(adc_data) > max_data_points:
                        adc_data.pop(0)

                    # Perbarui plot
                    line1.set_xdata(np.arange(len(x_data)))
                    line1.set_ydata(x_data)
                    ax1.set_xlim(0, max(len(x_data), max_data_points))

                    line2.set_xdata(np.arange(len(adc_data)))
                    line2.set_ydata(adc_data)
                    ax2.set_xlim(0, max(len(adc_data), max_data_points))

                    # Refresh plot
                    plt.draw()
                    plt.pause(0.05)

                except ValueError as e:
                    print(f"Kesalahan parsing data: {raw_line}, error: {e}")
            else:
                print(f"Format data tidak sesuai: {raw_line}")

except KeyboardInterrupt:
    print("Program dihentikan oleh pengguna.")

finally:
    ser.close()
    print("Koneksi serial ditutup.")
