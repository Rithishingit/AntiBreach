
import json
import random
import datetime
import time

# Configuration
LOG_SOURCES = ['web_server', 'firewall', 'ids']
EVENT_TYPES = {
    'web_server': ['login_success', 'login_failed', 'page_not_found'],
    'firewall': ['blocked_ip', 'allowed_ip'],
    'ids': ['intrusion_detected', 'suspicious_activity']
}
STATUS_CHOICES = ['success', 'failed', 'alert', 'info']

def generate_ip_address():
    """Generates a random IP address."""
    return f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

def generate_log_entry():
    """Generates a single cybersecurity log entry."""
    source = random.choice(LOG_SOURCES)
    event_type = random.choice(EVENT_TYPES[source])
    
    status = 'success'
    if 'failed' in event_type or 'blocked' in event_type:
        status = 'failed'
    elif 'intrusion' in event_type or 'suspicious' in event_type:
        status = 'alert'

    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "source": source,
        "ip_address": generate_ip_address(),
        "user_id": f"user_{random.randint(1000, 9999)}",
        "event_type": event_type,
        "status": status,
        "message": f"Log event of type {event_type} from {source}"
    }
    return log_entry

def generate_logs(num_logs=10):
    """Generates a list of cybersecurity logs."""
    logs = []
    for _ in range(num_logs):
        logs.append(generate_log_entry())
    return logs

if __name__ == "__main__":
    # Generate a stream of logs
    log_list = generate_logs(15)

    # Print logs in a JSON array format
    print(json.dumps(log_list, indent=4))

    # To generate logs continuously, you could use a loop like this:
    # try:
    #     while True:
    #         log = generate_log_entry()
    #         print(json.dumps(log))
    #         time.sleep(random.uniform(0.5, 2.0))
    # except KeyboardInterrupt:
    #     print("\nLog generation stopped.")

