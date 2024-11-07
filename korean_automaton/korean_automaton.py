import sys

CHOSUNG_LIST = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]
JUNGSUNG_LIST = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
]
JONGSUNG_LIST = [
    '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

ENG_TO_HANGUL = {
    'r': 'ㄱ', 'R': 'ㄲ', 's': 'ㄴ', 'e': 'ㄷ', 'E': 'ㄸ', 'f': 'ㄹ', 'a': 'ㅁ', 'q': 'ㅂ', 'Q': 'ㅃ', 't': 'ㅅ', 'T': 'ㅆ',
    'd': 'ㅇ', 'w': 'ㅈ', 'W': 'ㅉ', 'c': 'ㅊ', 'z': 'ㅋ', 'x': 'ㅌ', 'v': 'ㅍ', 'g': 'ㅎ',
    'k': 'ㅏ', 'o': 'ㅐ', 'i': 'ㅑ', 'O': 'ㅒ', 'j': 'ㅓ', 'p': 'ㅔ', 'u': 'ㅕ', 'P': 'ㅖ',
    'h': 'ㅗ', 'y': 'ㅛ', 'n': 'ㅜ', 'b': 'ㅠ', 'm': 'ㅡ', 'l': 'ㅣ',
    'hk': 'ㅘ', 'ho': 'ㅙ', 'hl': 'ㅚ', 'nj': 'ㅝ', 'np': 'ㅞ', 'nl': 'ㅟ', 'ml': 'ㅢ',
    'rt': 'ㄳ', 'sw': 'ㄵ', 'sg': 'ㄶ', 'fr': 'ㄺ', 'fa': 'ㄻ', 'fq': 'ㄼ', 'ft': 'ㄽ',
    'fx': 'ㄾ', 'fv': 'ㄿ', 'fg': 'ㅀ', 'qt': 'ㅄ'
}

COMPOSITE_FINALS = {
    'ㄺ': ('ㄹ', 'ㄱ'), 'ㄻ': ('ㄹ', 'ㅁ'), 'ㄼ': ('ㄹ', 'ㅂ'), 'ㄽ': ('ㄹ', 'ㅅ'),
    'ㄾ': ('ㄹ', 'ㅌ'), 'ㄿ': ('ㄹ', 'ㅍ'), 'ㅀ': ('ㄹ', 'ㅎ'), 'ㅄ': ('ㅂ', 'ㅅ'), 'ㄶ': ('ㄴ', 'ㅎ')
}

def combine_chosung_jungsung_jongsung(chosung, jungsung, jongsung=''):
    base_code = 0xAC00
    chosung_index = CHOSUNG_LIST.index(chosung)
    jungsung_index = JUNGSUNG_LIST.index(jungsung)
    jongseong_index = JONGSUNG_LIST.index(jongsung) if jongsung else 0
    char_code = base_code + (chosung_index * 21 * 28) + (jungsung_index * 28) + jongseong_index
    return chr(char_code)

def combine_hangul(input_str):
    result = ''
    i = 0
    converted_str = ''
    state = 0

    while i < len(input_str):
        if input_str[i] == ' ':
            converted_str += ' '
            i += 1
        elif input_str[i:i+2] in ENG_TO_HANGUL:
            converted_str += ENG_TO_HANGUL[input_str[i:i+2]]
            i += 2
        elif input_str[i] in ENG_TO_HANGUL:
            converted_str += ENG_TO_HANGUL[input_str[i]]
            i += 1
        else:
            converted_str += input_str[i]
            i += 1

    split_str = ""
    i = 0
    while i < len(converted_str):
        if converted_str[i] in COMPOSITE_FINALS and i + 1 < len(converted_str) and converted_str[i + 1] in JUNGSUNG_LIST:
            first_jongsung, second_chosung = COMPOSITE_FINALS[converted_str[i]]
            split_str += first_jongsung + second_chosung
            i += 1
        else:
            split_str += converted_str[i]
            i += 1

    i = 0
    while i < len(split_str):
        if split_str[i] == ' ':  # 공백 처리
            result += ' '
            i += 1
        elif split_str[i] in CHOSUNG_LIST:
            chosung = split_str[i]
            if i == len(split_str) - 1 or (i + 1 < len(split_str) and split_str[i + 1] not in JUNGSUNG_LIST):
                result += chosung  # 초성만 있어도 완성(Final State)
                i += 1
                continue
            if i + 1 < len(split_str) and split_str[i + 1] in JUNGSUNG_LIST:
                jungsung = split_str[i + 1]
                jongsung = ''
                
                if i + 2 < len(split_str) and split_str[i + 2] in JONGSUNG_LIST:
                    jongsung = split_str[i + 2]
                    if i + 3 < len(split_str) and split_str[i + 3] in JUNGSUNG_LIST:
                        result += combine_chosung_jungsung_jongsung(chosung, jungsung)
                        i += 3
                        continue
                    i += 3
                else:
                    i += 2
                result += combine_chosung_jungsung_jongsung(chosung, jungsung, jongsung)
            else:
                i += 1
        elif split_str[i] in JUNGSUNG_LIST:
            state = 1
            if(state == 1):
                state = 0
                i -= 1
        elif split_str[i] in JONGSUNG_LIST:
            if len(result) > 0 and '가' <= result[-1] <= '힣':
                prev_char = result[-1]
                prev_code = ord(prev_char) - 0xAC00
                prev_chosung_index = prev_code // (21 * 28)
                prev_jungsung_index = (prev_code % (21 * 28)) // 28
                new_char = combine_chosung_jungsung_jongsung(
                    CHOSUNG_LIST[prev_chosung_index],
                    JUNGSUNG_LIST[prev_jungsung_index],
                    split_str[i]
                )
                result = result[:-1] + new_char
                i += 1
            else:
                result += split_str[i]
                i += 1
    return result

test_input = sys.stdin.readline().rstrip()
test_output = combine_hangul(test_input)
sys.stdout.write(test_output)