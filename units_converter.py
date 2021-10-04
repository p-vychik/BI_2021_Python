import random

CONVERSION_COMMAND = {'PRESSURE','MASS','VOLUME', 'DISTANCE', 'EXIT'}

PRESSURE = {
        'bar':100000,
        'atmosphere':101325,
}

MASS = {
        'stone':6350.29318,
        'pound':453.59237,
        'ounce':28.349523125,
        'grain':0.006479891,
        'kg':1000,
        'carat':0.2,
}

VOLUME = {
        'barrel':119.240471,
        'gallon':3.785411784,
        'pint':0.473176473,
        'ounce':29.573531,
        'litre':1,
}
DISTANCE = {
        'km':1000,
        'yard':0.9144,
        'mile':1609.344,
        'inch':0.0254,
        'foot':0.3048,
}

def read_command():
    command = input('Choose what to convert:\n'
                      '     pressure;\n'
                      '     mass;\n'
                      '     volume;\n' 
                      '     distance;\n'
                      '     exit\n'
                    )
    return command.upper()


def command_check(command):
    if command not in CONVERSION_COMMAND:
        print(f"'{command.lower()}' - is incorrect command")
        return False
    else:
        return True


def conversion_check(conversion, command):
    fields = conversion.split(' ')
    if len(fields) != 4:
        return False
    if not fields[0].isnumeric:
        return False
    if not (fields[1] in eval(command) and fields[3] in eval(command)):
        return False
    return True


def make_convertation(command):
    print('supported conversions: ' + str(' '.join(eval(command).keys())))
    conversion = input(f"provide your command in the form '1 {random.choice(list(eval(command).keys()))}"
                       f" to {random.choice(list(eval(command).keys()))}'\n")
    while conversion_check(conversion, command) == False:
        conversion = input(f"Incorrect command, use the form '1 {random.choice(list(eval(command).keys()))}"
                       f" to {random.choice(list(eval(command).keys()))}'\n")
    fields = conversion.split(' ')
    result = (float(fields[0])*eval(command)[fields[1]])/(eval(command)[fields[3]])
    print(f"{fields[0]} {fields[1]} equals {result} {fields[3]}")


while True:
    command = read_command()
    if 'exit' in command:
        break
    else:
        while command_check(command) == False:
            command = read_command()
        if command == 'EXIT':
            print('Have a nice day!')
            break
        elif command == 'PRESSURE':
            make_convertation(command)
        elif command == 'MASS':
            make_convertation(command)
        elif command == 'TIME':
            make_convertation(command)
        elif command == 'VOLUME':
            make_convertation(command)
        elif command == 'DISTANCE':
            make_convertation(command)
