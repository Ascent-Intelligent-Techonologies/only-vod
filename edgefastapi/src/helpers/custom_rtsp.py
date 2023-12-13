import docker
import socket
from contextlib import closing




def create_new_rtsp_server(cameraname,original_url,port):
    
    client = docker.from_env()
    try:
        container = client.containers.get(f"""custom_{cameraname}""")
        container.remove(force=True)
    except:
        pass
        
    container = client.containers.run("camonitor-edge:custom-rtsp", "./mediamtx", detach=True, name=f"""custom_{cameraname}""", ipc_mode="host", ports={'8554/tcp':int(port)})
    container.exec_run(f"""ffmpeg -rtsp_transport tcp -i {original_url} -rtsp_transport tcp -c:v copy -f rtsp rtsp://127.0.0.1:8554/stream""", detach=True)
    
    return container.id

def is_port_available(port):
    
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex(("127.0.0.1", port)) == 0:
            return False
        else:
            return True
        