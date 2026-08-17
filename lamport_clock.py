class LamportClock:
    def __init__(self):
        self.time = 0

    # Increment clock for a local event
    def tick(self):
        self.time += 1
        return self.time

    # Increment clock before sending a message
    def send_event(self):
        self.time += 1
        return self.time

    # Update clock when receiving a message
    def receive_event(self, received_time):
        self.time = max(self.time, received_time) + 1
        return self.time

    def get_time(self):
        return self.time