#!/bin/bash
cd /home/zhaosheng/auto_booking_server && 
/opt/anaconda3/bin/python /home/zhaosheng/auto_booking_server/test.py --student_id 0 --place_num 3 --time 17 &\
/opt/anaconda3/bin/python /home/zhaosheng/auto_booking_server/test.py --student_id 1 --place_num 4 --time 17 &\
/opt/anaconda3/bin/python /home/zhaosheng/auto_booking_server/test.py --student_id 2 --place_num 5 --time 18 