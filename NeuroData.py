class NeuroData:
    def __init__(self, ID, attention_response, attention_rt, awareness_response,
                 awareness_rt, date, std_date, expName, session, trials_thisRepN,
                 trials_thisTrialN, trials_thisN, trials_thisIndex, key_presses,
                 other_keys_pressed):
        self.ID = ID
        self.attention_response = attention_response
        self.attention_rt = attention_rt
        self.awareness_response = awareness_response
        self.awareness_rt = awareness_rt
        self.date = date
        self.std_date = std_date
        self.expName = expName
        self.session = session
        self.trials_thisRepN = trials_thisRepN
        self.trials_thisTrialN = trials_thisTrialN
        self.trials_thisN = trials_thisN
        self.trials_thisIndex = trials_thisIndex
        self.key_presses = key_presses
        self.other_keys_pressed = other_keys_pressed
