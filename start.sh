  gnome-terminal -x bash -c "./src/resetf && exit; exec bash"\
& gnome-terminal -x bash -c "./src/fman; exec bash"\
& gnome-terminal -x bash -c "python3 ./src/sever_comm.py && exit; exec bash"\
& gnome-terminal -x bash -c "python3 ./src/sensor_reader.py && exit; exec bash"\
& gnome-terminal -x bash -c "python3 ./src/hardware_man.py && exit; exec bash"&
