# Abstract Reporter class
class Reporter:
    def report(self, parameter, breach):
        raise NotImplementedError("Subclasses should implement this method.")


# Example: List-based Reporter that stores messages in a list for later use
class ListReporter(Reporter):
    def __init__(self):
        self.reports = []

    def report(self, parameter, breach):
        # Append the report message to a list (no terminal output)
        self.reports.append({"parameter": parameter, "breach": breach})


# Example: File-based Reporter that writes reports to a file
class FileReporter(Reporter):
    def __init__(self, file_name):
        self.file_name = file_name

    def report(self, parameter, breach):
        # Write the report message to a file (no terminal output)
        with open(self.file_name, 'a') as f:
            f.write(f"{parameter} is {breach}!\n")


class BatteryChecker:
    def __init__(self, reporter=None):
        self.reporter = reporter or Reporter()

    def _check_parameter(self, parameter_name, value, min_value, max_value):
        if value < min_value:
            self.reporter.report(parameter_name, 'too low')
            return False
        if value > max_value:
            self.reporter.report(parameter_name, 'too high')
            return False
        return True

    def battery_is_ok(self, temperature, soc, charge_rate):
        return (
            self._check_parameter('Temperature', temperature, 0, 45) and
            self._check_parameter('State of Charge', soc, 20, 80) and
            self._check_parameter('Charge Rate', charge_rate, 0, 0.8)
        )


if __name__ == '__main__':
    # Example 1: Using ListReporter to store the reports in memory
    list_reporter = ListReporter()
    checker = BatteryChecker(list_reporter)
    
    assert(checker.battery_is_ok(25, 70, 0.7) is True)
    assert(checker.battery_is_ok(50, 85, 0) is False)   # Temperature too high, SOC too high

    # Access reports stored in ListReporter
    print("Stored reports:", list_reporter.reports)

    # Example 2: Using FileReporter to write reports to a file
    file_reporter = FileReporter("battery_log.txt")
    file_checker = BatteryChecker(file_reporter)
    
    assert(file_checker.battery_is_ok(-5, 70, 0.5) is False)  # Temperature too low

    # Check the contents of the "battery_log.txt" file for reports
