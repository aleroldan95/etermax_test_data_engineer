import os
import csv
import re

class DataCleaner():
    def __init__(self, input_file_path, file_name, output_file_path, input_encoding, delimiter, output_encoding, columns_conditions):
        self.input_file_path:str = input_file_path
        self.output_file_path:str = output_file_path
        self.input_encoding:str = input_encoding
        self.output_encoding:str = output_encoding
        self.file_name:str = file_name
        self.columns_conditions:{} = {i:cond for i, cond in enumerate(columns_conditions)}
        self.delimiter:str = delimiter

        self.run()

    def run(self):
        with open(self.input_file_path, 'r', encoding=self.input_encoding) as tsvf, \
                open(f'{self.output_file_path}/{self.file_name}.csv', 'w', newline='') as csvout:
            # CSV writer creator
            csvout = csv.writer(csvout, delimiter=self.delimiter)

            # Iterate through tsv rows with format validation
            for index, line in enumerate(csv.reader(tsvf, delimiter="\t")):

                if index==0:
                    # Header
                    csvout.writerow(line)
                else:
                    #Normal row
                    is_valid, line = self.is_valid_row(line)
                    if is_valid:
                        csvout.writerow(line)

    def is_valid_row(self, line):
        is_valid=True
        line_output=[]
        for i, text in enumerate(line):
            if self.columns_conditions[i] == 'int':
                #Integer column must have only numbers
                if not re.match(r'^([\s\d]+)$', text):
                    is_valid = False
                    break
                else:
                    line_output.append(text)
            elif self.columns_conditions[i] == 'str':
                #String column must have letters and start with upercase letter
                if not re.match('[a-zA-Z]', text):
                    is_valid = False
                    break
                else:
                    line_output.append(text.capitalize().strip())
            elif self.columns_conditions[i] == 'mail':
                #Mail column must have @
                if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
                    is_valid = False
                    break
                else:
                    line_output.append(text.strip())

        return is_valid, line_output

if __name__=='__main__':

    input_file_path = os.path.join(os.getcwd(), '..', 'instrucciones/datos_data_engineer.tsv')
    output_file_path = os.path.join(os.getcwd())

    DataCleaner(input_file_path=input_file_path,
                file_name='clean_data',
                output_file_path=output_file_path,
                input_encoding='utf-16-le',
                output_encoding='utf8',
                delimiter='|',
                columns_conditions=['int', 'str', 'str', 'int', 'mail'])
