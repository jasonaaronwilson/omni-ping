#!/usr/bin/env python3

targets = [
  "8.8.8.8",    # Google's public DNS
  "1.1.1.1",    # Cloudflare's DNS
  "192.168.1.1" # Example router IP (replace with your router's IP)
  ### "192.0.2.0",  # Unreachable address
]

import subprocess
import time
import datetime
import os

def ping_target(target):
  """Pings a target and returns the average RTT or None if failed."""
  try:
    # If you want more accuracy, then you can change the number of packets to something greater than '1'
    ping_output = subprocess.check_output(['ping', '-c', '1', target]).decode()
    rtt_line = [line for line in ping_output.split('\n') if 'rtt' in line][0]
    avg_rtt = float(rtt_line.split('=')[-1].split('/')[1])
    return avg_rtt
  except subprocess.CalledProcessError:
    return None

# Output format is "CDL" (C data-langugage aka comma-less JSON)
# {
#    target = "8.8.8.8"
#    status = reachable
#    rtt_ms = "31.83"
# }
#
# Or:
#
# {
#    target = "192.0.2.0"
#    status = unreachable
# }
# 
def to_record(timestamp, target, rtt):
    if rtt is None:
        return f'{{ timestamp = "{timestamp}" target = "{target}" status = unreachable }}'
    else:
        return f'{{ timestamp = "{timestamp}" target = "{target}" status = reachable rtt_ms = "{rtt:.2f}" }}'

### def to_record(timestamp, target, rtt):
###   # TODO(bard/gemini): FIXME!
###   if rtt is None:
###     return f"{timestamp} - {target} is unreachable!"
###   else:
###     return f"{timestamp} - {target} RTT: {rtt:.2f} ms"

def main():

  data_file = os.path.expanduser('~/omni-ping-data.cdl')

  while True:
      for target in targets:
          timestamp = datetime.datetime.now().isoformat()
          rtt = ping_target(target)
          print(to_record(timestamp, target, rtt))
          with open(data_file, 'a') as f:
              f.write(to_record(timestamp, target, rtt) + '\n')
      time.sleep(60)

if __name__ == "__main__":
  main()
