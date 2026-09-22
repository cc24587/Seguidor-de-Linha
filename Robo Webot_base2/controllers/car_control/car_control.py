#car_control controller
import struct 
import socket
import _thread

from controller import Robot, Camera, Display

status_sentido = False

# dados para criar um servidor socket para receber mensagens
def get_porta():
    return 9001
    
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255'),1)
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    return IP
    
def on_new_client(socket, addr):
    global status_sentido
    while True:
        msg = socket.recv(1024)
        if msg:
            print('chegou')
            break;
        else:
            break;
    req = msg.decode()
    if req.__contains__('anda'):
        status_sentido = True
    print(req)
    socket.close()
    return
    
# define o servidor
def servidor(https, hport):
    sockHttp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sockHttp.bind((https, hport))
    except:
        sockHttp.bind(('', hport))
        
    sockHttp.listen(1)
    print(f'Iniciou o servidor {get_ip()} na porta {get_porta()}')
    while True:
        client, addr = sockHttp.accept()
        _thread.start_new_thread(on_new_client, (client, addr))
        

# inicializa a thread do socket servidor
_thread.start_new_thread(servidor, (get_ip(), get_porta()))
robot = Robot()

timestep = int(robot.getBasicTimeStep())

print("Inicando rodas")
motorE = robot.getDevice('motorE')
motorD = robot.getDevice('motorD')
motorE.setPosition(float('inf'))
motorD.setPosition(float('inf'))
motorE.setVelocity(0.0)
motorD.setVelocity(0.0)

# OBTENDO E CONFIGURANDO SENSORES
ds = robot.getDevice('DS')
ds.enable(timestep)
ds2 = robot.getDevice('DS2')
ds2.enable(timestep)

dse = robot.getDevice('DSE')
dse.enable(timestep)
dsd = robot.getDevice('DSD')
dsd.enable(timestep)

# Ajuste para a camera
camera = robot.getDevice('camera')
refresh_rate_ms = 64
camera.enable(refresh_rate_ms)
# Ajuste do display
display = robot.getDevice('display')
print(display)

print("Iniciando...")
sentido = False
vini_e = 0
vini_d = 0

branco = 2.5
preto = 10.0
velocidade = 0.5
ganho = 0.5
while robot.step(timestep) != -1:  

    ve = round(dse.getValue(),2)
    vd = round(dsd.getValue(),2)
    
    leituraE = max(0.0, min(1.0, (ve - branco) / (preto - branco)))
    leituraD = max(0.0, min(1.0, (vd - branco) / (preto - branco)))
        
    correcao = ganho * (leituraE - leituraD)
    
    motorE.setVelocity(velocidade - correcao)
    motorD.setVelocity(velocidade + correcao)
    
    # value = ds.getValue()
    # value2 = ds2.getValue()
    
    # if value < 3.0:
       # print("mudou")
       # sentido = True
    # if value2 < 3.0:
       # print("mudou")
       # sentido = False
       
    # if sentido:
       # motorE.setVelocity(-1.0)
       # motorD.setVelocity(-1.0)
    # else:
       # motorE.setVelocity(1.0)
       # motorD.setVelocity(1.0)    
       
    # image = camera.getImage()
    # if display:
        # print('Display')
        # display.setImage(image)
        # print(image)
        
    # if status_sentido:
        # status_sentido = False
        # sentido = not sentido

# Enter here exit cleanup code.
