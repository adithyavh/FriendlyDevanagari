# All compounds are handled by underlying devanagari class, for eg: list("क्ष") = ["क", "्", "ष"]
VOWEL_MODIFIERS = {'ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'े', 'ै', 'ो', 'ौ'}
VOWELS = {'अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ', 'ओ', 'औ'}
CONSONANTS = {"क", "ख", "ग", "घ", "ङ", 
                  "च", "छ", "ज", "झ", "ञ", 
                  "ट", "ठ", "ड", "ढ", "ण", 
                  "त", "थ", "द", "ध", "न", 
                  "प", "फ", "ब", "भ", "म", 
                  "य", "र", "ल", "व", "श", "ष", "स", "ह", "ळ"} 


vowel__modifier = {
    "अ": "",
    "आ": "ा",
    "इ": "ि",
    "ई": "ी",
    "उ": "ु",
    "ऊ": "ू",
    "ऋ": "ृ",
    "ए": "े",
    "ऐ": "ै",
    "ओ": "ो",
    "औ": "ौ"
}

modifier__vowel = {
    '': 'अ',
    'ा': 'आ',
    'ि': 'इ',
    'ी': 'ई',
    'ु': 'उ',
    'ू': 'ऊ',
    'ृ': 'ऋ',
    'े': 'ए',
    'ै': 'ऐ',
    'ो': 'ओ',
    'ौ': 'औ'
}

VERB_GRADES_BEFORE_CONSONANTS= {}
VERB_GRADES_BEFORE_CONSONANTS.update({
    "अ": ["अ", "आ", "आ"],
    "इ": ["इ", "ए", "ऐ"],
    "ई": ["ई", "ए", "ऐ"],
    "उ": ["उ", "ओ", "औ"],
    "ऊ": ["ऊ", "ओ", "औ"],
    "ऋ": ["ऋ", "अर्", "आर्"],
    "ऐ": ["ऐ", "आय्", "आय्"], # Verify with an expert
})
for vowel in list(VERB_GRADES_BEFORE_CONSONANTS.keys()):
    VERB_GRADES_BEFORE_CONSONANTS[vowel__modifier[vowel]] = VERB_GRADES_BEFORE_CONSONANTS[vowel]

VERB_GRADES_BEFORE_VOWELS = {}
VERB_GRADES_BEFORE_VOWELS.update({
    "अ": ["अ", "आ", "आ"],
    "इ": ["इ", "अय्", "आय्"],
    "ई": ["ई", "अय्", "आय्"],
    "उ": ["उ", "अव्", "आव्"],
    "ऊ": ["ऊ", "अव्", "आव्"],
    "ऋ": ["ऋ", "अर्", "आर्"],
    "ऐ": ["ऐ", "आय्", "आय्"], # Verify with an expert
})
for vowel in list(VERB_GRADES_BEFORE_VOWELS.keys()):
    VERB_GRADES_BEFORE_VOWELS[vowel__modifier[vowel]] = VERB_GRADES_BEFORE_VOWELS[vowel]

VERB_GRADES_BEFORE_CONSONANTS, VERB_GRADES_BEFORE_VOWELS

VOWELS_GRADES = set(VERB_GRADES_BEFORE_VOWELS.keys())

# For internal sandhi only

AA_VOWEL_SANDHI = {
    "अ": {
        'अ': 'आ',
        'आ': 'आ',
        'इ': 'ए',
        'ई': 'ए',
        'उ': 'ओ',
        'ऊ': 'ओ',
        'ऋ': 'अर्',
        'ए': 'ऐ',
        'ऐ': 'ऐ',
        'ओ': 'औ',
        'औ': 'औ'
    },
    "आ": {
        'अ': 'आ',
        'आ': 'आ',
        'इ': 'ए',
        'ई': 'ए',
        'उ': 'ओ',
        'ऊ': 'ओ',
        'ऋ': 'अर्',
        'ए': 'ऐ',
        'ऐ': 'ऐ',
        'ओ': 'औ',
        'औ': 'औ'
    },
}

# First vowel is not अ or आ
OTHER_VOWEL_SANDHI = {
    "इ": "य्",
    "ई": "य्",
    "उ": "व्",
    "ऊ": "व्",
    "ऋ": "र्",
    "ए": "अय्",
    "ऐ": "आय्",
    "ओ": "अव्",
    "औ": "आव्"
}

class DevanagariString:
    def __init__(self, string: str):
        self.string = string

    def __repr__ (self):
      return self.string
    
    def __str__ (self):
      return self.string
    
    def _is_last_char_vowel(self):
        return self.string[-1] in VOWELS or self.string[-1] in VOWEL_MODIFIERS

    def _is_first_char_vowel(self):
        return self.string[0] in VOWELS or self.string[0] in VOWEL_MODIFIERS

    def __add__(self, otherString):

        # CLEANING
        # --------

        # Convert other string to a devanagari string object if not already
        if isinstance(otherString, str):
            otherString = DevanagariString(otherString)

        # If the first character of the second string is a vowel modifier, convert it to a vowel
        if len(otherString.string)>0 and otherString.string[0] in VOWEL_MODIFIERS:
            otherString.string = modifier__vowel[otherString.string[0]] + otherString.string[1:]
        
        # TRIVIAL OPERATIONS
        # ------------------

        # 1: First string is empty
        if self.string == "":
            return DevanagariString(otherString.string)
        
        # 2: Second string is empty
        elif otherString.string == "":
            return DevanagariString(self.string)
        
        # CORE OPERATIONS
        # ---------------
        
        # 3: Consonant end + Vowel beginning
        
        if self.string[-1] == "्" and otherString.string[0] in VOWELS:
            self.string = self.string[:-1]
            otherString.string = vowel__modifier[otherString.string[0]]+ otherString.string[1:]
            return DevanagariString(self.string + otherString.string)
        
        # 4: Pure Vowel + Vowel beginning

        elif self.string[-1] in VOWELS and otherString._is_first_char_vowel():
            if self.string[-1] in AA_VOWEL_SANDHI:
                return DevanagariString(self.string[:-1] + AA_VOWEL_SANDHI[self.string[-1]][otherString.string[0]] + otherString.string[1:])
            else:
                return DevanagariString(self.string[:-1] + OTHER_VOWEL_SANDHI[self.string[-1]][:-1] + vowel__modifier[otherString.string[0]] + otherString.string[1:])
        
        # 5: Vowel modifier end + Vowel beginning

        elif (self.string[-1] in VOWEL_MODIFIERS or self.string[-1] in CONSONANTS) and otherString._is_first_char_vowel(): # check for pure consonant = check for अ
            
            if self.string[-1] in CONSONANTS: # Actually ends in अ ("a")
                return DevanagariString(self.string + vowel__modifier[AA_VOWEL_SANDHI["अ"][otherString.string[0]]] + otherString.string[1:])
            else:
                vowel = modifier__vowel[self.string[-1]]
                if vowel == "आ":
                    return DevanagariString(self.string[:-1] + vowel__modifier[AA_VOWEL_SANDHI[vowel][otherString.string[0]]] + otherString.string[1:])
                else: # Recursive call for simpler addition case
                    return DevanagariString(self.string[:-1] + "्") + DevanagariString(OTHER_VOWEL_SANDHI[vowel][:-1] + vowel__modifier[otherString.string[0]] + otherString.string[1:])

        # 6. Consontant end + Consonant beginning
        else:
            return DevanagariString(self.string + otherString.string)

# TESTS

# 1: First string is empty
a = DevanagariString("")
b = DevanagariString("अ")
c = a + b
assert c.string == "अ", c

# 2: Second string is empty
a = DevanagariString("अ")
b = DevanagariString("")
c = a + b
assert c.string == "अ", c

# 3: Consonant end + Vowel beginning
a = DevanagariString("क्")
b = DevanagariString("अ")
c = a + b
assert c.string == "क", c

# 4: Pure Vowel + Vowel beginning
a = DevanagariString("अ")
b = DevanagariString("अ")
c = a + b
assert c.string == "आ", c

a = DevanagariString("अ")
b = DevanagariString("ई")
c = a + b
assert c.string == "ए", c

a = DevanagariString("अ")
b = DevanagariString("ऊ")
c = a + b
assert c.string == "ओ", c

a = DevanagariString("इ")
b = DevanagariString("अम्बा")
c = a + b
assert c.string == "यम्बा", c

a = DevanagariString("ए")
b = DevanagariString("उत्तम")
c = a + b
assert c.string == "अयुत्तम", c

a = DevanagariString("ऐ")
b = DevanagariString("उपरि")
c = a + b
assert c.string == "आयुपरि", c

# 5: Vowel modifier end + Vowel beginning

a = DevanagariString("वानर")
b = DevanagariString("आगम")
c = a + b
assert c.string == "वानरागम", c

a = DevanagariString("सीता")
b = DevanagariString("अगम")
c = a + b
assert c.string == "सीतागम", c

a = DevanagariString("वानरी")
b = DevanagariString("आगम")
c = a + b
assert c.string == "वानर्यागम", c

a = DevanagariString("सीते")
b = DevanagariString("उपरि")
c = a + b
assert c.string == "सीतयुपरि", c
