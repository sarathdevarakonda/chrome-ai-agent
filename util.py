import io
import csv

def to_csv_data(headers,data):
        csv_buffer = csv.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=headers)
        writer.writeheader()
        for item in data:
            writer.writerow(item)

        # Get CSV data as a string
        csv_data = csv_buffer.getvalue()
        return csv_data