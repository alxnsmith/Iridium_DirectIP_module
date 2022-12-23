from iridium.services.Messages import MT_Message

test_message = bytes().fromhex(
    '01002D4100154D73673133303030333430313031323334353000004213494D4549333030303334303130313233343530')


def test_parse_mt_message():
    print('Test MT_Message:', test_message)
    mt_message = MT_Message(test_message)
    parsed_message = mt_message.parse()
    print('Parsed MT_Message:', parsed_message)
    print()
    print('Message value      :', mt_message.make())
    print('Test Message value :', test_message)
    assert mt_message.make() == test_message, "Message is not equal to test message"


def test_make_mt_message():
    msg = MT_Message.create('Msg1', '300034010123450',
                            b'\x00\x00', "IMEI300034010123450")
    print('Created MT_Message:', msg)
    print('Parsed MT_Message:', MT_Message(msg.make()).parse())
    print()
    print('Message value      :', msg.make())
    print('Test Message value :', test_message)
    assert msg.make() == test_message, "Message is not equal to test message"
