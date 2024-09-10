import csv
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class FlowLogsProcessor:
    """
    A class to process flow logs and generate summaries based on a lookup table.
    """

    # Class constant for protocol mapping
    PROTOCOL_MAP = {
        '6': 'tcp',
        '17': 'udp',
        '1': 'icmp',
        # Add other protocols as needed
    }

    def __init__(self, lookup_table_path: str, flow_logs_path: str, output_path: str):
        """
        Initialize the FlowLogsProcessor with file paths.

        :param lookup_table_path: Path to the lookup table CSV file
        :param flow_logs_path: Path to the flow logs text file
        :param output_path: Path to the output CSV file
        """
        self.lookup_table_path = lookup_table_path
        self.flow_logs_path = flow_logs_path
        self.output_path = output_path

    @staticmethod
    def create_directory(file_path: str) -> None:
        """
        Create the parent directory for a given file path if it doesn't exist.

        :param file_path: Path to the file
        """
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    def process_flow_logs(self) -> List[Tuple[str, str]]:
        """
        Process the flow logs file and extract required data.

        :return: List of tuples containing (destination port, protocol number)
        """
        required_flow_data = []
        try:
            with open(self.flow_logs_path, 'r') as file:
                for line_number, line in enumerate(file, 1):
                    try:
                        fields = line.strip().split()
                        if len(fields) < 8:
                            print(f"Warning: Line {line_number} has insufficient fields. Skipping.")
                            continue
                        required_flow_data.append((fields[6], fields[7]))
                    except IndexError:
                        print(f"Error: Line {line_number} is malformed. Skipping.")
                return required_flow_data
        except FileNotFoundError:
            print(f"Error: Flow log file '{self.flow_logs_path}' not found.")
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied when trying to read '{self.flow_logs_path}'.")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred while reading the flow log file: {e}")
            sys.exit(1)

    def read_lookup_table(self) -> Dict[Tuple[str, str], str]:
        """
        Read the lookup table CSV file and create a mapping.

        :return: Dictionary mapping (port, protocol) to tag
        """
        lookup_data = {}
        try:
            with open(self.lookup_table_path, 'r') as data:
                reader = csv.reader(data)
                next(reader)  # Skip the header row
                for row_number, row in enumerate(reader, 2):
                    if len(row) != 3:
                        print(f"Warning: Row {row_number} in lookup table has incorrect number of fields. Skipping.")
                        continue
                    port, protocol, tag = row
                    lookup_data[(port, protocol.lower())] = tag
                return lookup_data
        except FileNotFoundError:
            print(f"Error: Lookup table file '{self.lookup_table_path}' not found.")
            sys.exit(1)
        except PermissionError:
            print(f"Error: Permission denied when trying to read '{self.lookup_table_path}'.")
            sys.exit(1)
        except csv.Error as e:
            print(f"Error: CSV file '{self.lookup_table_path}' is malformed: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred while reading the lookup table: {e}")
            sys.exit(1)

    def match_flowdata_tags(self, flow_data: List[Tuple[str, str]], lookup_table: Dict[Tuple[str, str], str]) -> Tuple[
        Dict[str, int], Dict[Tuple[str, str], int]]:
        """
        Match flow data with tags and count occurrences.

        :param flow_data: List of (destination port, protocol number) tuples
        :param lookup_table: Dictionary mapping (port, protocol) to tag
        :return: Tuple of (tag counts, port/protocol counts)
        """
        tag_count = {}
        portprotocol_count = {}
        for dst_port, protocol_num in flow_data:
            try:
                protocol_name = self.PROTOCOL_MAP.get(protocol_num, protocol_num).lower()
                key = (dst_port, protocol_name)

                # Count port/protocol combinations
                portprotocol_count[key] = portprotocol_count.get(key, 0) + 1

                # Look up and count tags
                tag = lookup_table.get(key, "Untagged")
                tag_count[tag] = tag_count.get(tag, 0) + 1
            except Exception as e:
                print(f"Error processing entry {dst_port}, {protocol_num}: {e}")
        return tag_count, portprotocol_count

    def write_results_to_csv(self, tag_counts: Dict[str, int], portprotocol_counts: Dict[Tuple[str, str], int]) -> None:
        """
        Write the results to the output CSV file.

        :param tag_counts: Dictionary of tag counts
        :param portprotocol_counts: Dictionary of port/protocol combination counts
        """
        self.create_directory(self.output_path)
        with open(self.output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Tag Counts:'])
            writer.writerow(['Tag', 'Count'])
            for tag, count in tag_counts.items():
                writer.writerow([tag, count])

            writer.writerow([])  # Empty row for separation
            writer.writerow(['Port/Protocol Combination Counts:'])
            writer.writerow(['Port', 'Protocol', 'Count'])
            for (port, protocol), count in portprotocol_counts.items():
                writer.writerow([port, protocol, count])

    def generate_output(self) -> None:
        """
        Main method to process flow logs and generate the output file.
        """
        try:
            lookup_data = self.read_lookup_table()
            flow_data = self.process_flow_logs()
            tag_counts, portprotocol_counts = self.match_flowdata_tags(flow_data, lookup_data)
            self.write_results_to_csv(tag_counts, portprotocol_counts)
            print(f"Results have been written to {self.output_path}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)


def main():
    """
    Main entry point of the script.
    """
    processor = FlowLogsProcessor(
        lookup_table_path='input_files/lookup_table.csv',
        flow_logs_path='input_files/flow_logs.txt',
        output_path='out/output.csv'
    )
    processor.generate_output()


if __name__ == "__main__":
    main()
