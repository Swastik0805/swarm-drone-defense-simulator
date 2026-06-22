class Radar:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.range = 350

    def detect_intruders(self, intruders):

        detected = []

        for intruder in intruders:

            distance = (
                ((intruder.x - self.x) ** 2) +
                ((intruder.y - self.y) ** 2)
            ) ** 0.5

            if distance <= self.range:

                detected.append(intruder)

        return detected