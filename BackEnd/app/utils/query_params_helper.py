import re

class QueryParamHelper:
    @staticmethod
    def convert_query_param_to_tuples(param):
        # Extract all the numbers from the string using regular expressions
        numbers = re.findall(r'[\d\.]+', param)

        # Convert the numbers to ints and group them into tuples
        tuples = [(round(float(numbers[i])), round(float(numbers[i+1]))) for i in range(0, len(numbers), 2)]

        return tuples
