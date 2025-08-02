'''
    Jonathan Christen
    2025
'''
url_replace_bible_number = "$bible_number$"
url_replace_bible        = "$version$"
url_replace_book         = "$book$"
url_replace_chapter      = "$chapter$"
url_base = 'https://www.bible.com/es/bible/$bible_number$/$book$.$chapter$.$version$'

parser_data = {'chapter_title_start': '<div class="ChapterContent_reader__Dt27r"><h1>',
               'chapter_title_end':   '</h1>',
               'verse_number_start':  'R2PLt\">',
               'verse_start':         'RrUqA\">',
               'verse_end':           '</span>',
               'verses_end':          '</path></svg>'}

language_specific = {
        'spanish': {'language_icons': ['Spanish', 'spanish', 'Español', 'español'],
                    'version':        'Biblia   |',
                    'book':           'Libre    |',
                    'chapter':        'Capitulo |',
                    'chapter_header': 'Capitulo'},
        'english': {'language_icons': ['English', 'english'],
                    'version':        'Version |',
                    'book':           'Book    |',
                    'chapter':        'Chapter |',
                    'chapter_header': 'Chapter'},
        'arabic':  {'language_icons': ['Arabic', 'arabic', 'العريه', 'عريه'],
                    'version':        'بداية | ',
                    'book':           'كتب   | ',
                    'chapter':        'الفصل | ',
                    'chapter_header': 'الفصل'} }

books_table = [
        "GEN",
        "EXO",
        "LEV",
        "NUM",
        "DEU",
        "JOS",
        "JDG",
        "RUT",
        "1SA",
        "2SA",
        "1KI",
        "2KI",
        "1CH",
        "2CH",
        "EZR",
        "NEH",
        "EST",
        "JOB",
        "PSA",
        "PRO",
        "ECC",
        "SNG",
        "ISA",
        "JER",
        "LAM",
        "EZK",
        "DAN",
        "HOS",
        "JOL",
        "AMO",
        "OBA",
        "JON",
        "MIC",
        "NAM",
        "HAB",
        "ZEP",
        "HAG",
        "ZEC",
        "MAL",
        "MAT",
        "MRK",
        "LUK",
        "JHN",
        "ACT",
        "ROM",
        "1CO",
        "2CO",
        "GAL",
        "EPH",
        "PHP",
        "COL",
        "1TH",
        "2TH",
        "1TI",
        "2TI",
        "TIT",
        "PHM",
        "HEB",
        "JAS",
        "1PE",
        "2PE",
        "1JN",
        "2JN",
        "3JN",
        "JUD",
        "REV"
]

disjoined_words = [
        ["S", "eñor"],
        ["D", "ios"],
        ["L", "ord"]
        ]
