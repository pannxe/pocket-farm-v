  gnome-terminal -x bash -c "/home/pi/Desktop/PocketFarm-linux/resetf && exit; exec bash"\
& gnome-terminal -x bash -c "/home/pi/Desktop/PocketFarm-linux/fman; exec bash"\
& gnome-terminal -x bash -c "python3 /home/pi/Desktop/PocketFarm-linux/sever_comm.py && exit; exec bash"\
& gnome-terminal -x bash -c "python3 /home/pi/Desktop/PocketFarm-linux/sensor_reader.py && exit; exec bash"\
& gnome-terminal -x bash -c "python3 /home/pi/Desktop/PocketFarm-linux/hardware_man.py && exit; exec bash"&
