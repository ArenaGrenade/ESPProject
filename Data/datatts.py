import json

class toThingSpeak():
    def __init__(self, labels):
        self.data = []
        self.labels = labels

    def add(self, values):
        if(isinstance(values, list)):
            if(isinstance(values[0], list)):
                for value in values:
                    self.add(value)
            elif(len(self.labels) == len(values)):
                tmp = {}
                for ind, label in enumerate(self.labels):
                    tmp[label] = values[ind]
                self.data.append(tmp)
            else:
                raise ValueError("Input length does not match label length")
        else:
            raise ValueError("Input should be a list")

    def print(self, indent=None):
        print(json.dumps(self.data, indent=indent))

    def save(self, path):
        with open(path, 'w') as f:
            json.dump(self.data, f, indent=4)

if __name__ == "__main__":
    tts = toThingSpeak(["created_at", "entry_id", "field1", "field2", "field3", "field4", "field5", "field6", "field7"])
    tts.add(["2021-12-04T12:50:01Z", 1, "24.50000", "56.40000", "0.83333", "422.00000", "3.00000", "30163", "35"])
    # tts.print(1)
    tts.save("Synthetic/log1.json")