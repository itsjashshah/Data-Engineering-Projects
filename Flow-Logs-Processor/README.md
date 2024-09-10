# Flow Logs Processor

## Description
This program parses Flow log data and maps each row to a tag based on a lookup table. It processes the flow logs, matches them against the lookup table, and generates a report with tag counts and port/protocol combination counts.

## Assumptions and Requirements
- The code was developed and tested on Python 3.12.5, but should be compatible with Python 3.6+.
- The program uses the sample input files provided in the assessment as default.
- Input files (flow logs and lookup table) are correctly formatted:
  - No leading or trailing spaces in the text file or CSV.
  - No extra spaces in the middle of lines in the text file.
  - All fields in the CSV file are correctly separated by commas.
- The flow log file follows the AWS VPC Flow Logs format (version 2).
- The lookup table CSV file has three columns: dstport, protocol, and tag.
- The maximum file size for flow logs is 10 MB.
- The lookup table can have up to 10,000 mappings.
- Tags can map to more than one port/protocol combination.
- Matches are case-insensitive.

## Prerequisites
- Python 3.6 or higher
- No additional libraries required (uses only Python standard library)

## Build & Run

### 1. Create a Virtual Environment (Optional but recommended)
```sh
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 2. Run the Script
```sh
python solution.py
```

## Input Files
- Place your flow logs file as `input_files/flow_logs.txt`
- Place your lookup table as `input_files/lookup_table.csv`

## Output
The program generates `out/output.csv` containing:
- Count of matches for each tag
- Count of matches for each port/protocol combination

## Limitations
- Only supports default log format (version 2) for Flow Logs.
- Does not handle custom log formats.

## Manual Testing Performed

While formal unit tests have not been implemented, the following manual tests were conducted to ensure the program's functionality and robustness:

1. Input Validation:
   - Verified correct parsing of well-formatted input files.
   - Tested error handling for malformed flow logs and lookup tables.

2. File Processing:
   - Confirmed successful processing of flow log files up to 10 MB.
   - Validated handling of lookup tables with 10,000 entries.

3. Error Handling:
   - Tested program behavior with non-existent input files.
   - Verified appropriate error messages for various IO exceptions.

4. Data Mapping and Counting:
   - Manually verified correct tag assignment and counting for a sample dataset.
   - Checked accurate counting of port/protocol combinations.

5. Edge Cases:
   - Tested with empty input files.
   - Verified handling of flow log entries not matching any lookup table entry.

6. Output Verification:
   - Confirmed correct format and content of the output CSV file.
   - Validated tag counts and port/protocol combination counts for known inputs.

These manual tests were performed to ensure the program meets the specified requirements and handles various scenarios correctly. Future improvements could include implementing automated unit tests and more comprehensive integration tests.

## Additional Analysis

- Memory Efficiency: The program processes flow logs line by line, allowing it to handle large files without loading the entire content into memory.
- Scalability: The use of dictionaries for lookup and counting operations provides efficient performance even with large datasets.
- Error Handling: Comprehensive error handling is implemented to gracefully manage various potential issues, such as file I/O errors or malformed input data.
- Modularity: The code is structured into clear, separate methods, enhancing readability and maintainability.
- Standard Library Usage: By utilizing only Python's standard library, the program maintains high portability and ease of setup across different environments.

## Author
Jash Shah
