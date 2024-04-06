import ftplib

#TODO: account for duplicate file names
#TODO: get img from data_process folder
#TODO: Dale we need to talk ablout the directory structure for the ftp server and how we will handle the data locally
host = '153.92.9.132'
username = 'u274618925.rpi_client'
password = 'Rpigaitinsight!05'

#this works
#dir structure for gaitinsight should be /rpi_data/patient_id/date/video_id/frame_id.jpg
#root for this ftp server is /rpi_data
ftpserver = ftplib.FTP(host, username, password)

ftpserver.encoding = 'utf-8'

filename = 'test_img.jpg'

#send image to server
with open(filename, 'rb') as file:
    ftpserver.storbinary('STOR ' + filename, file)

ftpserver.dir()
ftpserver.quit()