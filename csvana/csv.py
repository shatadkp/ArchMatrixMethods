import pandas as pd
from collections import Counter
import argparse
import sys

def analyze_csv(file_path, output_path):
    try:
        # Read the CSV file into a pandas DataFrame
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty.")
        sys.exit(1)
    except pd.errors.ParserError:
        print(f"Error: The file '{file_path}' does not appear to be in CSV format.")
        sys.exit(1)
    
    # Open the output file in write mode
    with open(output_path, 'w') as f:
        # Iterate through each column
        for column in df.columns:
            f.write(f"Column: '{column}'\n")
            # Drop NaN values for analysis
            column_data = df[column].dropna()
            total_values = len(column_data)
            unique_values = column_data.unique()
            num_unique = len(unique_values)
            
            if num_unique == total_values:
                f.write("  All values are unique.\n\n")
            else:
                f.write("  Repeated values:\n")
                # Count occurrences using Counter
                counts = Counter(column_data)
                # Filter out values that occur only once
                repeated = {k: v for k, v in counts.items() if v > 1}
                for value, count in repeated.items():
                    f.write(f"    {value}: {count} times\n")
                f.write("\n")
    
    print(f"Analysis complete. Results have been written to '{output_path}'.")

def main():
    parser = argparse.ArgumentParser(description="Analyze CSV columns for unique and repeated values.")
    parser.add_argument('csv_file', help='Path to the CSV file to analyze.')
    parser.add_argument('-o', '--output', default='analysis_results.txt', help='Path to the output text file.')
    
    args = parser.parse_args()
    analyze_csv(args.csv_file, args.output)

if __name__ == "__main__":
        main()
