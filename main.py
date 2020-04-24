from binparse import BinaryParse
import json


def result_json(file_name):
    def decorator(fn):
        def wrapper():
            """Decorator provide functionality to output dictionary as JSON to file"""
            try:
                if not isinstance(file_name, str):
                    raise TypeError('Var file_name must be string')
                result = fn()
                result = json.dumps(result, indent=4)
                with open(file_name, 'w') as file:
                    file.write(result)
                return result
            except (TypeError, OSError) as e:
                print(e.args[0])
                exit(1)
        return wrapper
    return decorator


@result_json('./results')
def main():
    binparse = BinaryParse('/home/sergey/Документы/Development/Source/binary_parse/ansible-role-php-master.zip')
    # result = binparse.find_pattern({
    #     '504B0304': 'zip'
    # })

    result = binparse.find_repeat_sequences(3)

    return result


if __name__ == '__main__':
    main()