class Observer:
    def update(self, event_type, data):
        """
        React to a notification from the Subject.
        :param event_type: A string describing the type of event (e.g., "pellet_collected").
        :param data: Additional data relevant to the event.
        """
        raise NotImplementedError("Observer subclasses must implement the 'update' method.")

class Subject:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        """Register an observer."""
        self.observers.append(observer)

    def remove_observer(self, observer):
        """Unregister an observer."""
        self.observers.remove(observer)

    def notify_observers(self, event_type, data):
        """Notify all observers of an event."""
        for observer in self.observers:
            observer.update(event_type, data)
