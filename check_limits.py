
class Reporter:
    def report(self, parameter, breach):
        print(f"{parameter} is {breach}!")

class BatteryChecker:
    def __init__(self, reporter=None):
        self.reporter = reporter or Reporter()

    def check_parameter(self, parameter_name, value, min_value, max_value):
        if value < min_value:
            self.reporter.report(parameter_name, 'too low')
            return False
        if value > max_value:
            self.reporter.report(parameter_name, 'too high')
            return False
        return True

    def battery_is_ok(self, temperature, soc, charge_rate):
        return (
            self.check_parameter('Temperature', temperature, 0, 45) and
            self.check_parameter('State of Charge', soc, 20, 80) and
            self.check_parameter('Charge Rate', charge_rate, 0, 0.8)
        )

if __name__ == '__main__':
    checker = BatteryChecker()
    
    assert(checker.battery_is_ok(25, 70, 0.7) is True)
    assert(checker.battery_is_ok(50, 85, 0) is False)   # Temperature too high, SOC too high
    assert(checker.battery_is_ok(-5, 70, 0.5) is False)  # Temperature too low
    assert(checker.battery_is_ok(30, 85, 0.5) is False)  # SOC too high
    assert(checker.battery_is_ok(30, 70, 0.9) is False)  # Charge rate too high
    assert(checker.battery_is_ok(25, 70, 0.8) is True)   # All within range
    assert(checker.battery_is_ok(0, 20, 0.8) is True)    # Boundary conditions lower
    assert(checker.battery_is_ok(45, 80, 0.8) is True)   # Boundary conditions upper
    assert(checker.battery_is_ok(0, 19, 0.8) is False)   # SOC too low
    assert(checker.battery_is_ok(0, 20, 0.9) is False)   # Charge rate too high


