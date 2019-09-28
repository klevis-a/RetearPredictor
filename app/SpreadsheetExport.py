import io
import csv


def write_csv(json_entries, dict_fields, col_names):
    string_buffer = io.StringIO()
    csv_writer = csv.DictWriter(string_buffer, fieldnames=dict_fields)
    csv_writer.writer.writerow(col_names)
    csv_writer.writerows(json_entries)
    return string_buffer.getvalue().encode('utf-8')
