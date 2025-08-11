# day7_hl7_parser.py

def parse_hl7_message(file_path):
    with open(file_path, 'r') as f:
        message = f.read().strip()

    segments = message.split('\n')

    parsed_message = {}
    for segment in segments:
        fields = segment.split('|')
        segment_name = fields[0]

        # For each field, handle repeating fields (~) and components (^)
        parsed_fields = []
        for field in fields[1:]:
            repetitions = field.split('~')
            parsed_reps = []
            for rep in repetitions:
                components = rep.split('^')
                if len(components) > 1:
                    parsed_reps.append(components)
                else:
                    parsed_reps.append(rep)
            parsed_fields.append(parsed_reps)

        parsed_message[segment_name] = parsed_fields

    return parsed_message


if __name__ == "__main__":
    file_path = 'sample-hl7-messages/day7_sample_message.hl7'
    parsed = parse_hl7_message(file_path)

    print("Parsed HL7 Message:")
    for segment, fields in parsed.items():
        print(f"{segment}:")
        for i, repetitions in enumerate(fields, 1):
            print(f"  Field {i}:")
            for rep in repetitions:
                if isinstance(rep, list):
                    print(f"    Components: {rep}")
                else:
                    print(f"    Value: {rep}")
        print()

