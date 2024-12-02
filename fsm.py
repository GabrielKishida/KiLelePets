class State:
    def __init__(self, name):
        self.name = name
        self.transitions = {}

    def add_transition(self, event, state):
        self.transitions[event] = state

    def on_event(self, event):
        return self.transitions.get(event, self)
    
    def get_transitions(self):
        return self.transitions

    def do(self):
        return

class FSM:
    def __init__(self, initial_state):
        self.current_state = initial_state

    def transition(self, event):
        next_state = self.current_state.on_event(event)
        if next_state != self.current_state:
            print(f"Transitioning from {self.current_state.name} to {next_state.name}")
        else:
            print(f"No transition for event '{event}' from state {self.current_state.name}")
        self.current_state = next_state
    
    def update(self):
        result = self.current_state.do()
        if result is not None:                
            found = any(result in sublist for sublist in self.current_state.get_transitions().keys())
            if found:
                self.transition(result)
