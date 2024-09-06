import os
import subprocess
import time

processes = []
num_streams = int(os.getenv('NUM_STREAMS', 10))
sink_type = os.getenv('SINK_TYPE', 'rtsp')


def _start_single_stream(pipeline):
    print(f'starting pipeline: {pipeline}')
    process = subprocess.Popen(['gst-launch-1.0', '-e'] + pipeline.split(' '))
    setattr(process, 'pipeline', pipeline)
    processes.append(process)


def check_processes():
    for p in [p for p in processes]:
        poll = p.poll()
        if poll is not None:
            print(f'process for pipeline `{p.pipeline}` has died, restarting...')
            processes.remove(p)
            _start_single_stream(p.pipeline)
            print('restarted process successfully')


def generate_opus_streams_rtsp():
    rtsp_server = os.getenv('RTSP_SERVER', 'localhost:8554') 
    
    for i in range(num_streams):
        pipeline = f'audiotestsrc ! audioconvert ! audioresample ! opusenc ! queue ! rtspclientsink location=rtsp://{rtsp_server}/{i}'
        _start_single_stream(pipeline)
        

def generate_opus_streams_udp():
    sink_host = os.getenv('SINK_HOST', '127.0.0.1')
    sink_start_port = os.getenv('SINK_START_PORT', 20000)
    
    for i in range(num_streams):
        pipeline = f'audiotestsrc ! audioconvert ! audioresample ! audio/x-raw, rate=24000 ! opusenc ! rtpopuspay ! queue ! udpsink host={sink_host} port={sink_start_port + i}'
        _start_single_stream(pipeline)


def generate_opus_streams():
    if sink_type == 'rtsp':
        generate_opus_streams_rtsp()
    elif sink_type == 'udp':
        generate_opus_streams_udp()
    else:
        raise ValueError('Invalid sink type')


if __name__ == '__main__':
    generate_opus_streams()
    while True:
        time.sleep(30)
        print('checking pipeline processes...')
        check_processes()
