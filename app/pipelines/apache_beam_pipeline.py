import apache_beam as beam


def pipeline(input_path, output_path):
    with beam.Pipeline() as p:
        (
            p
            | "Read files" >> beam.io.ReadFromText(input_path)
            | "Process" >> beam.Map(lambda x: x.upper())
            | "Write files" >> beam.io.WriteToText(output_path)
        )
