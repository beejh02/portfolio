# 초성, 중성, 종성 리스트 정의
CHOSUNG_LIST = [
    'ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]
JUNGSUNG_LIST = [
    'ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ'
]
JONGSUNG_LIST = [
    '', 'ㄱ', 'ㄲ', 'ㄳ', 'ㄴ', 'ㄵ', 'ㄶ', 'ㄷ', 'ㄹ', 'ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅁ', 'ㅂ', 'ㅄ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ'
]

# 영문 입력을 한글 자모로 변환하는 매핑 테이블
ENG_TO_HANGUL = {
    'r': 'ㄱ', 'R': 'ㄲ', 's': 'ㄴ', 'e': 'ㄷ', 'E': 'ㄸ', 'f': 'ㄹ', 'a': 'ㅁ', 'q': 'ㅂ', 'Q': 'ㅃ', 't': 'ㅅ', 'T': 'ㅆ',
    'd': 'ㅇ', 'w': 'ㅈ', 'W': 'ㅉ', 'c': 'ㅊ', 'z': 'ㅋ', 'x': 'ㅌ', 'v': 'ㅍ', 'g': 'ㅎ',
    'k': 'ㅏ', 'o': 'ㅐ', 'i': 'ㅑ', 'O': 'ㅒ', 'j': 'ㅓ', 'p': 'ㅔ', 'u': 'ㅕ', 'P': 'ㅖ',
    'h': 'ㅗ', 'y': 'ㅛ', 'n': 'ㅜ', 'b': 'ㅠ', 'm': 'ㅡ', 'l': 'ㅣ',
    'hk': 'ㅘ', 'ho': 'ㅙ', 'hl': 'ㅚ', 'nj': 'ㅝ', 'np': 'ㅞ', 'nl': 'ㅟ', 'ml': 'ㅢ',
    'rt': 'ㄳ', 'sw': 'ㄵ', 'sg': 'ㄶ', 'fr': 'ㄺ', 'fa': 'ㄻ', 'fq': 'ㄼ', 'ft': 'ㄽ',
    'fx': 'ㄾ', 'fv': 'ㄿ', 'fg': 'ㅀ', 'qt': 'ㅄ'
}

def eng_to_hangul(eng_str):
    hangul_str = ''
    skip = 0
    for i in range(len(eng_str)):
        if skip > 0:
            skip -= 1
            continue
        # 복합 종성 조합을 확인하고 분리하여 처리
        if i + 1 < len(eng_str) and eng_str[i:i+2] in ENG_TO_HANGUL:
            if eng_str[i:i+2] in ['fr', 'fa', 'fq', 'ft', 'fx', 'fv', 'fg', 'rt', 'sw', 'sg', 'qt']:
                # 복합 종성을 구성하는 문자 각각을 처리
                hangul_str += ENG_TO_HANGUL[eng_str[i]]  # 첫 번째 문자는 종성으로 처리
                hangul_str += ENG_TO_HANGUL[eng_str[i + 1]]  # 두 번째 문자는 초성으로 처리
                skip = 1
            else:
                hangul_str += ENG_TO_HANGUL[eng_str[i:i+2]]
                skip = 1
        elif eng_str[i] in ENG_TO_HANGUL:
            hangul_str += ENG_TO_HANGUL[eng_str[i]]
        else:
            hangul_str += eng_str[i]
    return hangul_str

def combine_chosung_jungsung_jongsung(chosung, jungsung, jongsung=''):
    # 유니코드 한글 계산 공식 적용
    base_code = 0xAC00
    chosung_index = CHOSUNG_LIST.index(chosung)
    jungsung_index = JUNGSUNG_LIST.index(jungsung)
    jongseong_index = JONGSUNG_LIST.index(jongsung) if jongsung else 0
    
    # 한글 코드 계산
    char_code = base_code + (chosung_index * 21 * 28) + (jungsung_index * 28) + jongseong_index
    return chr(char_code)

def combine_hangul(input_str):
    result = ''
    i = 0
    while i < len(input_str):
        if input_str[i] in CHOSUNG_LIST:
            chosung = input_str[i]
            if i + 1 < len(input_str) and input_str[i + 1] in JUNGSUNG_LIST:
                jungsung = input_str[i + 1]
                jongsung = ''
                if i + 2 < len(input_str) and input_str[i + 2] in JONGSUNG_LIST:
                    jongsung = input_str[i + 2]
                    i += 3
                else:
                    i += 2
                result += combine_chosung_jungsung_jongsung(chosung, jungsung, jongsung)
            else:
                # 중성이 없으면 초성만 처리하고 다음 문자로 이동
                result += chosung
                i += 1
        elif input_str[i] in JUNGSUNG_LIST:
            # 중성 문자 처리
            if len(result) > 0 and result[-1] >= '가' and result[-1] <= '힣':
                prev_char = result[-1]
                prev_code = ord(prev_char) - 0xAC00
                prev_chosung_index = prev_code // (21 * 28)
                prev_jungsung_index = (prev_code % (21 * 28)) // 28
                prev_jongsung_index = (prev_code % 28)

                # 종성이 있는 경우, 종성을 다음 초성으로 이동
                if prev_jongsung_index != 0:
                    # 종성을 분리하여 처리
                    new_char = combine_chosung_jungsung_jongsung(
                        CHOSUNG_LIST[prev_chosung_index],
                        JUNGSUNG_LIST[prev_jungsung_index]
                    )
                    result = result[:-1] + new_char
                    chosung = JONGSUNG_LIST[prev_jongsung_index]
                    if chosung not in CHOSUNG_LIST:
                        # 초성으로 사용할 수 없는 경우 기본 초성으로 대체
                        chosung = 'ㅇ'
                    jungsung = input_str[i]
                    jongsung = ''
                    if i + 1 < len(input_str) and input_str[i + 1] in JONGSUNG_LIST:
                        jongsung = input_str[i + 1]
                        i += 1
                    result += combine_chosung_jungsung_jongsung(chosung, jungsung, jongsung)
                else:
                    chosung = 'ㅇ'
                    jungsung = input_str[i]
                    result += combine_chosung_jungsung_jongsung(chosung, jungsung)
            else:
                result += combine_chosung_jungsung_jongsung('ㅇ', input_str[i])
            i += 1
        elif input_str[i] in JONGSUNG_LIST:
            if len(result) > 0 and result[-1] >= '가' and result[-1] <= '힣':
                prev_char = result[-1]
                prev_code = ord(prev_char) - 0xAC00
                prev_chosung_index = prev_code // (21 * 28)
                prev_jungsung_index = (prev_code % (21 * 28)) // 28

                # 복합 종성 처리
                if input_str[i] in ['ㄺ', 'ㄻ', 'ㄼ', 'ㄽ', 'ㄾ', 'ㄿ', 'ㅀ', 'ㅄ']:
                    # 복합 종성을 분리하여 종성과 초성으로 처리
                    jongsung = input_str[i][0]  # 첫 번째 자모를 종성으로 사용
                    new_char = combine_chosung_jungsung_jongsung(
                        CHOSUNG_LIST[prev_chosung_index],
                        JUNGSUNG_LIST[prev_jungsung_index],
                        jongsung
                    )
                    result = result[:-1] + new_char
                    # 두 번째 자모를 초성으로 사용 (예: ㄺ에서 ㄱ은 초성)
                    next_chosung = input_str[i][1] if len(input_str[i]) > 1 else ''
                    if next_chosung and next_chosung in CHOSUNG_LIST:
                        result += next_chosung
                else:
                    new_char = combine_chosung_jungsung_jongsung(
                        CHOSUNG_LIST[prev_chosung_index],
                        JUNGSUNG_LIST[prev_jungsung_index],
                        input_str[i]
                    )
                    result = result[:-1] + new_char
                i += 1
            else:
                chosung = input_str[i]
                if chosung in JONGSUNG_LIST:
                    # 초성으로 사용할 수 없는 종성을 기본 초성으로 대체
                    chosung = 'ㅇ'
                if i + 1 < len(input_str) and input_str[i + 1] in JUNGSUNG_LIST:
                    jungsung = input_str[i + 1]
                    result += combine_chosung_jungsung_jongsung(chosung, jungsung)
                    i += 2
                else:
                    result += chosung
                    i += 1
        else:
            result += input_str[i]
            i += 1
    return result

# 테스트 코드
input_str = str(input())
hangul_str = eng_to_hangul(input_str)
result = combine_hangul(hangul_str)

print(result)
