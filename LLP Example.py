# nepieciešamie procesi
from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime
# Local timestamp
# Ar šīs koda daļas palīdzību galarezultātam tiks pievienota gan lamporta pulksteņa pozīcija, gan procesa pulksteņa vērtība.
def local_time(counter):
    return '(Lamport_time={}, Local_time={})'. format(counter, datetime.now())
# New timestamp when a message is recieved
# Šajā koda daļā tiek ietverta informācija par to, ka izmainīsies laika vērtības, notiekot kādam notikumam.
def calc_recv_timestamp(recv_time_stamp, counter):
    return max(recv_time_stamp, counter) + 1
# Nākamajās trīs koda daļās tiek definēti notikumi kādi var notikt starp procesiem, tiek definēts notikums kā tāds, ziņojuma nosūtīšanas notikums un ziņojuma saņemšanas notikums.
# Funckija visiem iespējamajiem notikumiem
def event(pid, counter):
    counter += 1
    print('Something happened in {} !'.\
          format(pid) + local_time(counter))
    return counter

# Ziņas nosūtīšanas notikums.
def send_message(pipe, pid, counter):
    counter += 1
    pipe.send(('Empty shell', counter))
    print('Message sent from ' + str(pid) + local_time(counter))
    return counter

# Ziņas saņemšanas notikums.
def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    print('Message recieved at ' + str(pid) + local_time(counter))
    return counter
# Procesu definēšana
# Šeit notiek procesu definēšana starp kuriem notiks notikumi. Vispirms kodā tiek ietverts tas ka katram procesam būs savs ID kods.
# Šeit jāņem vērā arī tas, ka katru reizi kad kods tiek palaists no jauna, katram procesam būs cits ID kods.
# Tad tiek ierakstīta informācija par katru iespējamo notikumu.
def process_one(pipe12):
    pid = getpid()
    counter = 0
    counter = event(pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    counter = event(pid, counter)

def process_two(pipe21, pipe23):
    pid = getpid()
    counter = 0
    counter = recv_message(pipe21, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    counter = recv_message(pipe23, pid, counter)

def process_three(pipe32):
    pid = getpid()
    counter = 0
    counter = recv_message(pipe32, pid, counter)
    counter = send_message(pipe32, pid, *counte*)

# Procesu izveide
# Šajā koda daļā tiek izveidoti paši procesi starp kuriem notiks notikumi.
if __name__ == '__main__':

    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_one,
                       args=(oneandtwo,))
    process2 = Process(target=process_two,
                       args=(twoandone, twoandthree))
    process3 = Process(target=process_three,
                       args=(threeandtwo,))
# Šī koda daļa ir svarīga, jo bez šīs koda daļas kods nestrādās pareizi. Šī koda daļa nodrošina to, lai notiktu procesi kā arī lai tiktu iziets no koda rezultātu loga pēc koda pilnīgas izpildes.
# Lai būtu iespējams aplūkot rezultātu ir iespējams Piespiest kodam pārtraukt izpildi un uzrādīt kļūdu(Tas ir redzams koda 59 rindiņā)
    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()
