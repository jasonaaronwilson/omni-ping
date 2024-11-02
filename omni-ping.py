#!/usr/bin/env python3

# List of target IP addresses or hostnames to ping
targets = [
  "8.8.8.8",    # Google's public DNS
  "1.1.1.1",    # Cloudflare's DNS
  "192.168.86.1" # My "Google Home" router. Your Mileage May Vary
  ### "192.0.2.0",  # Typically an unreachable address (useful for testing).
]

import subprocess
import time
import datetime
import os

def ping_target(target):
  """Pings a target and returns the average round-trip time (RTT).

    Args:
      target: The IP address or hostname to ping.

    Returns:
      The average RTT in milliseconds as a float, or None if the ping failed.
  """
  try:
    # If you want more accuracy, then you can change the number of packets to something greater than '1'
    ping_output = subprocess.check_output(['ping', '-c', '1', target]).decode()
    rtt_line = [line for line in ping_output.split('\n') if 'rtt' in line][0]
    avg_rtt = float(rtt_line.split('=')[-1].split('/')[1])
    return avg_rtt
  except subprocess.CalledProcessError:
    return None

def to_record(timestamp, target, rtt):
  """Formats ping results into a CDL (comma-less JSON) record.

    Args:
      timestamp: The timestamp of the ping.
      target: The target IP address or hostname.
      rtt: The average round-trip time or None if unreachable.

    Returns:
      A string representing the ping result in CDL format.

    Examples:
      '{ timestamp = "2024-11-01T22:30:00" target = "8.8.8.8" status = reachable rtt_ms = "31.83" }'
      '{ timestamp = "2024-11-01T22:30:00" target = "192.0.2.0" status = unreachable }'
    """
  if rtt is None:
    return f'{{ timestamp = "{timestamp}" target = "{target}" status = unreachable }}'
  else:
    return f'{{ timestamp = "{timestamp}" target = "{target}" status = reachable rtt_ms = "{rtt:.2f}" }}'

def main():
  """Main function to continuously ping targets and log results."""

  # Path to the data file where ping results will be stored.
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
