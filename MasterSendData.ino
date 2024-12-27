#include <Wire.h>
#include <MPU6050.h>

// Buat objek MPU6050
MPU6050 mpu;

// Rumus konversi untuk akselerometer (MPU6050)
const float MPU6050_SENSITIVITY = 16384.0; // Sensitivitas akselerometer (untuk resolusi ±2g)

void setup() {
  // Mulai komunikasi serial dan I2C
  Serial.begin(115200);
  Wire.begin();
  
  // Inisialisasi sensor MPU6050
  mpu.initialize();
  
  // Cek apakah MPU6050 berhasil terhubung
  if (mpu.testConnection()) {
    Serial.println("MPU6050 terhubung dengan sukses!");
  } else {
    Serial.println("Gagal terhubung ke MPU6050");
    while (1); // Hentikan eksekusi jika gagal terhubung
  }
}

void loop() {
  // Variabel untuk menyimpan data akselerasi
  int16_t ax, ay, az;  // Akselerasi sumbu X, Y, Z
  
  // Membaca data akselerasi dari sensor
  mpu.getAcceleration(&ax, &ay, &az);
  
  // Mengonversi nilai akselerasi menjadi tegangan
  // Dengan menggunakan ADC pada sumbu X (misalnya, akselerometer X)
  
  // Konversi nilai akselerasi (dalam raw values) ke dalam satuan 'g' (gravitasi)
  float ax_g = ax / MPU6050_SENSITIVITY; // Menghitung akselerasi pada sumbu X dalam 'g'
  
  // Menampilkan data akselerometer hanya untuk sumbu X dalam satuan 'g'
  Serial.print("Accelerometer X (g): ");
  Serial.println(ax_g, 3);  // Menampilkan dengan 3 angka di belakang koma
  
  // Membaca nilai ADC dari pin A0 (misalnya)
  int adcValue = analogRead(A0);
  
  // Mengonversi nilai ADC menjadi tegangan (referensi 3.3V, dengan resolusi 12 bit untuk ADC)
  // Pada 12 bit ADC, rentang nilai adalah 0-4095
  float voltage = (adcValue / 4095.0) * 3.3;  // Mengonversi nilai ADC menjadi tegangan
  
  // Menampilkan nilai ADC dan tegangan  
  // Menunggu sejenak sebelum mengambil data lagi
  delay(100);
}