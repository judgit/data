def id_string(s):
    s = s.translate({
        ord('０'): '0',
        ord('１'): '1',
        ord('２'): '2',
        ord('３'): '3',
        ord('４'): '4',
        ord('５'): '5',
        ord('６'): '6',
        ord('７'): '7',
        ord('８'): '8',
        ord('９'): '9',
        ord(':'): '',
    })
    return '{:04}'.format(int(s))


def text_content(selector):
    text = ''.join(selector.getall())
    return text.replace('\r\n', ' ').strip()
