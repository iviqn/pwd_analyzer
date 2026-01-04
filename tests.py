from password_analyzer import PasswordAnalyzer

def test_has_dg(analyzer):
    analyzer.has_digits("ojub91bei")
    analyzer.has_digits("aadjrfr")

def test_has_upplw(analyzer):
    analyzer.has_upper("abcdefg")
    analyzer.has_lower("uuudbapfr")

def test_has_spc(analyzer):
    analyzer.has_special("abc!")
    analyzer.has_special("abc123")

def test_pwdsizerate(analyzer):
    analyzer.basic_rating("uia")
    analyzer.basic_rating("Abcdef123!@#")

def test_has_repeat(analyzer):
    analyzer.has_repeat("aaaBBB")
    analyzer.has_repeat("aB3$k9")

def test_patterns(analyzer):
    analyzer.has_common_pattern("password123")
    analyzer.has_common_pattern("flgke[r]")
    analyzer.has_common_pattern("X9$kLmP2!")

def test_popular(analyzer):
    analyzer.pops("password")

def test_has_leak(analyzer):
    analyzer.leaks("qwerty")

def test_phonetic(analyzer):
    analyzer.phonetics("banana")
    analyzer.phonetics("xqzptk")

def test_basic_analyze_runs(analyzer):
    analyzer.basic_analyze(")fnqkb4")
