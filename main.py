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


@result_json('./results.json')
def main():
    binparse = BinaryParse('file_name')
    # result = binparse.find_pattern({
    #     '504B0304': 'zip',
    #     '42F0FBB21BE9': 'test1'
    # })

    result = binparse.find_zip_archives()

    return result


if __name__ == '__main__':
    main()