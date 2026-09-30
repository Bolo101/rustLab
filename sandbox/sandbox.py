class Temperature:
    def __init__(self, temperature):
        self.temperature = temperature

    def to_farenheit(self):
        return (self.temperature * 9/5) + 32

    def __str__(self):
        return f"The temperature is {self.temperature}°C"

temp = Temperature(25)
print(f"Temperature in Celsius: {temp}")
print(f"Temperature in Fahrenheit: {temp.to_farenheit()}°F")    