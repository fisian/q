# set of possible interpreter states
states = {"error":-1, "action": 0, "type": 1, "value": 2, "block": 3}
# action resolving

actionModifiers = {
        "none": 1,
        "if": 2,
        "while": 3
    }
# type resolving
types = {
        "error":-1,
        "blockbegin": 1,
        "blockend": 2,
        "eval": 3,
        "+Number": 4,
        "-Number": 5,
        "lChar": 6,
        "uChar": 7,
        "sChar": 8,
        "Number": "NUMBER",
        "String": "STRING"
    }
sChars = " !\n\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"
