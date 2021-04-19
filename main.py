from rotors import *


def rotor_generator(initial_position=(0, 0, 0)):
    # generates rotors according to the positions
    a = Rotor1[initial_position[0]:] + Rotor1[:initial_position[0]]
    b = Rotor1[initial_position[1]:] + Rotor1[:initial_position[1]]
    c = Rotor1[initial_position[2]:] + Rotor1[:initial_position[2]]
    rotor1 = dict([(list(alphabets)[i], a[i]) for i in range(26)])
    rotor2 = dict([(list(alphabets)[i], b[i]) for i in range(26)])
    rotor3 = dict([(list(alphabets)[i], c[i]) for i in range(26)])
    reflector = dict([(list(alphabets)[i], list(Reflector)[i]) for i in range(26)])
    return dict([('rotor1', rotor1), ('rotor2', rotor2), ('rotor3', rotor3), ('reflector', reflector)])


def plugboard(plugin=''):
    # takes a string as input and makes it into a dict and returns it
    if plugin != None:
        a = plugin.split(' ')
        b = {}
        for i in a:
            b[i.split(':')[0].upper()] = i.split(':')[1].upper()
        return b


def machine(message, option, plugin=None, intial_position=(0, 0, 0)):
    r1 = intial_position[0]
    r2 = intial_position[1]
    r3 = intial_position[2]
    plugin = plugboard(plugin)
    cipher_text = ''
    for i in message.upper().replace(' ', ''):
        rotor1 = rotor_generator((r1, r2, r3))['rotor1']
        rotor2 = rotor_generator((r1, r2, r3))['rotor2']
        rotor3 = rotor_generator((r1, r2, r3))['rotor3']
        # rf for reflected rotor
        rfrotor1 = dict([(value, key) for key, value in rotor1.items()])
        rfrotor2 = dict([(value, key) for key, value in rotor2.items()])
        rfrotor3 = dict([(value, key) for key, value in rotor3.items()])
        rfplugin = dict([(value, key) for key, value in plugin.items()])
        reflector = rotor_generator()['reflector']

        if plugin != None and i in plugin.keys() and option.upper() == 'E':
            cipher_text = cipher_text + rfrotor1[rfrotor2[rfrotor3[reflector[rotor3[rotor2[rotor1[plugin[i]]]]]]]]
        elif i in rfplugin.keys() and option.upper() == 'E':
            cipher_text = cipher_text + rfrotor1[rfrotor2[rfrotor3[reflector[rotor3[rotor2[rotor1[rfplugin[i]]]]]]]]
        else:
            cipher_text = cipher_text + rfrotor1[rfrotor2[rfrotor3[reflector[rotor3[rotor2[rotor1[i]]]]]]]

        r1 = r1 + 1
        # rotating rotor for every alphabet
        if r1 == 26:
            r1 = 0
            r2 = r2 + 1
        if r2 == 26:
            r2 = 0
            r3 = r3 + 1
    if option.upper() == 'D':
        rfplugin = dict([(value, key) for key, value in plugin.items()])
        d = ''
        for c in cipher_text:
            if c in rfplugin.keys():
                d += rfplugin[c]
            elif c in plugin.keys():
                d += plugin[c]
            else:
                d += c
        return d

    return cipher_text


if __name__ == '__main__':
    # your message as first argument
    # e for encryption and d for decryption as second argument
    # plugboard input as shown (make sure you don't repeat a single alphabet twice) you can use lower case but format must be same
    # a tuple of initial position as third argument
    print(machine('your message here', 'e', 'A:R F:W S:Q C:P', (5, 12, 0)))
    print(machine('ZBMCPQIFQTMGHTD', 'd', 'A:R F:W S:Q C:P', (5, 12, 0)))

