from iridium.services.Messages import MO_Message


test_message = bytes().fromhex(
    '01004A01001CC7C8836433303032333430363930303236333000049B0000550705B303000B004422675339760000000402001A04070120A9050755300F98D40F046001F604330000C007341300')


def test_parse_MO_Message():
    print('Test MO message:', test_message)
    mo_message = MO_Message(test_message)
    mo_message_parsed = mo_message.parse()
    print('Parsed MO message:', mo_message_parsed)
    assert mo_message.make() == test_message, 'MO message parsing failed'
