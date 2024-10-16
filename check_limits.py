class Reporter:
    def report(self, parameter, message):
        raise NotImplementedError("Subclasses should implement this method.")


class ListReporter(Reporter):
    def __init__(self):
        self.reports = []

    def report(self, parameter, message):
        self.reports.append({"parameter": parameter, "message": message})


class FileReporter(Reporter):
    def __init__(self, file_name):
        self.file_name = file_name

    def report(self, parameter, message):
        with open(self.file_name, 'a') as f:
            f.write(f"{parameter}: {message}\n")


class BatteryChecker:
    def __init__(self, reporter=None):
        self.reporter = reporter or Reporter()

    def _calculate_warning_range(self, min_value, max_value, tolerance_percent):
        """Calculate the warning range based on the tolerance."""
        tolerance = tolerance_percent / 100 * max_value
        return (min_value, min_value + tolerance), (max_value - tolerance, max_value)

    def _check_parameter(self, parameter_name, value, min_value, max_value, enable_warning):
        """Check if the value is within limits and report warnings if enabled."""
        if value < min_value:
            self.reporter.report(parameter_name, "too low")
            return False
        if value > max_value:
            self.reporter.report(parameter_name, "too high")
            return False

        if enable_warning:
            low_warning, high_warning = self._calculate_warning_range(min_value, max_value, 5)
            if low_warning[0] <= value < low_warning[1]:
                self.reporter.report(parameter_name, "Approaching discharge")
            if high_warning[0] < value <= high_warning[1]:
                self.reporter.report(parameter_name, "Approaching charge-peak")

        return True

    def battery_is_ok(self, temperature, soc, charge_rate):
        """Main function to validate battery parameters."""
        return (
            self._check_parameter('Temperature', temperature, 0, 45, enable_warning=True) and
            self._check_parameter('State of Charge', soc, 20, 80, enable_warning=True) and
            self._check_parameter('Charge Rate', charge_rate, 0, 0.8, enable_warning=False)
        )


if __name__ == '__main__':
    # Test with ListReporter
    list_reporter = ListReporter()
    checker = BatteryChecker(list_reporter)

    assert checker.battery_is_ok(22, 21, 0.7) is True  # Warning for SOC should be reported
    assert checker.battery_is_ok(50, 85, 0) is False    # Temperature & SOC too high

    print("Stored reports:", list_reporter.reports)

    # Test with FileReporter
    file_reporter = FileReporter("battery_log.txt")
    file_checker = BatteryChecker(file_reporter)

    assert file_checker.battery_is_ok(-5, 70, 0.5) is False  # Temperature too low
