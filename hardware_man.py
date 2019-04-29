from Flag import Flag
import RPi.GPIO as GPIO
import common_flags as cf
import time

fan_pin = 21
water_pin = 20
light_pin = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(fan_pin, GPIO.OUT, initial = 0)
GPIO.setup(water_pin, GPIO.OUT, initial = 0)
GPIO.setup(light_pin, GPIO.OUT, initial = 0)


def main():
	cur_set_f = open('now_setting.conf', 'r')
	cur_setting = cur_set_f.readline().split()
	
	r_flag = Flag(open("request.flg", "r+"))
	b_flag = Flag(open("busy.flg", "r+"))
	a_flag = Flag(open("answer.flg", "r+"))
    
	b_flag.get_data()
	while b_flag.is_busy():
		time.sleep(0.5)
		b_flag.get_data()
	b_flag.flag_f.close()
	
	r_flag.set_stat([cf.Comp.OUTPUT, cf.Stat.REQUESTED, 0, 0, 0, 0, 0, 0])
    
	while True:
		a_flag.flag_f = open("answer.flg", "r+")
		r_flag.flag_f = open("request.flg", "r+")
		a_flag.get_data()
		r_flag.get_data()
        
		if a_flag.is_answered() and r_flag.buffer:
			r_flag.set_stat([cf.Comp.OUTPUT, cf.Stat.ACQUIRED, 0, 0, 0, 0, 0, 0])
			d_flag = Flag(open("sensor_data.flg", "r"))
			now_stat = d_flag.get_data()
			del d_flag
			break
			
		r_flag.flag_f.close()
		a_flag.flag_f.close()
		time.sleep(1)
	print("now stat: " + str(now_stat))
	print("cur :     " + str(cur_setting))
	# Light
	if bool(cur_setting[cf.Env.lumi]) :
		GPIO.output(light_pin, GPIO.LOW)
	else :
		GPIO.output(light_pin, GPIO.HIGH)
		
	# Water
	if float(now_stat[6]) <= float(cur_setting[cf.Env.mois])-10:
		GPIO.output(water_pin, GPIO.HIGH)
		time.sleep(7)
		GPIO.output(water_pin, GPIO.LOW)
		
	# Fan
	if float(now_stat[2]) > float(cur_setting[cf.Env.humi]) and float(now_stat[4]) < float(now_stat[2]):
		GPIO.output(fan_pin, GPIO.HIGH)
		time.sleep(3)
		GPIO.output(fan_pin, GPIO.LOW)
	
	time.sleep(1)
	
while True:
	main()
