class Reporter:
    """Base class for all reporters."""
    def report(self, parameter, message):
        raise NotImplementedError("Subclasses should implement this method.")


class ListReporter(Reporter):
    """Reporter that stores reports in memory for testing."""
    def __init__(self):
        self.reports = []

    def report(self, parameter, message):
        self.reports.append({"parameter": parameter, "message": message})


class FileReporter(Reporter):
    """Reporter that logs reports to a file."""
    def __init__(self, file_name):
        self.file_name = file_name

    def report(self, parameter, message):
        with open(self.file_name, 'a') as f:
            f.write(f"{parameter}: {message}\n")


class BatteryChecker:
    """Class to check battery parameters and generate reports."""

    def __init__(self, reporter=None):
        self.reporter = reporter or Reporter()

    def _calculate_tolerance(self, max_value, tolerance_percent=5):
        """Calculate tolerance based on the percentage of the max value."""
        return (tolerance_percent / 100) * max_value

    def _within_warning_range(self, value, min_value, max_value, tolerance):
        """Check if value falls within the warning range."""
        low_warning, high_warning = min_value + tolerance, max_value - tolerance
        if min_value <= value < low_warning:
            return "Approaching discharge"
        elif high_warning < value <= max_value:
            return "Approaching charge-peak"
        return None

    def _check_value(self, parameter_name, value, min_value, max_value, enable_warning):
        """Evaluate if the parameter value is within acceptable limits."""
        if value < min_value:
            self.reporter.report(parameter_name, "too low")
            return False
        elif value > max_value:
            self.reporter.report(parameter_name, "too high")
            return False

        if enable_warning:
            tolerance = self._calculate_tolerance(max_value)
            warning_message = self._within_warning_range(value, min_value, max_value, tolerance)
            if warning_message:
                self.reporter.report(parameter_name, warning_message)

        return True

    def battery_is_ok(self, temperature, soc, charge_rate):
        """Check all battery parameters."""
        return all([
            self._check_value('Temperature', temperature, 0, 45, enable_warning=True),
            self._check_value('State of Charge', soc, 20, 80, enable_warning=True),
            self._check_value('Charge Rate', charge_rate, 0, 0.8, enable_warning=False)
        ])


if __name__ == '__main__':
    # Test with ListReporter
    list_reporter = ListReporter()
    checker = BatteryChecker(list_reporter)

    assert checker.battery_is_ok(22, 21, 0.7) is True  # Warning for SOC
    assert checker.battery_is_ok(50, 85, 0) is False    # Temperature & SOC too high

    print("Stored reports:", list_reporter.reports)

    # Test with FileReporter
    file_reporter = FileReporter("battery_log.txt")
    file_checker = BatteryChecker(file_reporter)

    assert file_checker.battery_is_ok(-5, 70, 0.5) is False  # Temperature too low
