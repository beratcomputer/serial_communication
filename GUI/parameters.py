






class Stewart_Parameters:
    # updateMoment = 1: when reboot, 0: immidiatly
    def __init__(self, isWriteable, isReadeable, updateMoment:int=0) -> None:
        self.isWriteable = isWriteable
        self.isReadeable = isReadeable
        self.updateMoment = 0
