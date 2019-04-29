from Flag import Flag
import serial
import common_flags as cf
import time


def read_sensor():
    d_flag = Flag(open("sensor_data.flg", "w"))
    
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    while ser.in_waiting == 0:
        time.sleep(0.25)
    line = ser.readline().decode("utf-8").split()
    while len(line) < 5:
         line = ser.readline().decode("utf-8").split()

    print(str(line))
    in_humi, in_temp, mois = line[0], line[1], line[2]
    out_humi, out_temp = line[3], line[4]
    
    lumi = 1
    d_flag.set_stat([
        cf.Comp.INPUT, cf.Stat.ANSWERED,
        in_humi, in_temp,
        out_humi, out_temp,
        mois, lumi
    ])
    del d_flag


def ready_stat():
    ia_flag = Flag(open("ians.flg", "r+"))
    ia_flag.set_stat([cf.Comp.INPUT, cf.Stat.READY, 0, 0, 0, 0, 0, 0])
    del ia_flag


def write_stat():
    ia_flag = Flag(open("ians.flg", "r+"))
    ia_flag.set_stat([cf.Comp.INPUT, cf.Stat.ANSWERED, 0, 0, 0, 0, 0, 0])
    del ia_flag


print("Pocket Farm's")
print("SENSOR READER MODULE\nVERSION 1.0.0")
print("_________________________\n")
ir_flag = Flag(open("ireq.flg", "r+"))
first = False
while True:
    ir_flag.flag_f = open("ireq.flg", "r+")
    ir_flag.get_data()
    if ir_flag.is_requested() and not first:
        print("Reading... ", end="")
        read_sensor()
        write_stat()
        print("done")
        first = True

    if ir_flag.is_acquired() and first:
        ready_stat()
        first = False
        print("acquired")
    
    ir_flag.flag_f.close()
    time.sleep(1)
