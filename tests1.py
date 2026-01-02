from password_analyzer import PasswordAnalyzer


def test_has_digits(analyzer):
    analyzer.has_digits("ojub91bei")
    analyzer.has_digits("aadjrfr")


def test_has_upper_lower(analyzer):
    analyzer.has_upper("abcdefg")
    analyzer.has_lower("uuudbapfr")


def test_has_special(analyzer):
    analyzer.has_special("abc!")
    analyzer.has_special("abc123")


def test_password_length_rating(analyzer):
    analyzer.basic_rating("uia")
    analyzer.basic_rating("Abcdef123!@#")


def test_repeated_chars(analyzer):
    analyzer.has_repeat("aaaBBB")
    analyzer.has_repeat("abc123")
    analyzer.has_repeat("aB3$k9")


def test_common_patterns(analyzer):
    analyzer.has_common_pattern("password123")
    analyzer.has_common_pattern("flgke[r]")
    analyzer.has_common_pattern("X9$kLmP2!")


def test_popular_exact(analyzer):
    analyzer.pops("password")


def test_popular_similar(analyzer):
    analyzer.pops("mypassword123")


def test_local_leak_found(analyzer):
    analyzer.leaks("qwerty")

def test_phonetic_easy(analyzer):
    analyzer.phonetics("banana")


def test_phonetic_hard(analyzer):
    analyzer.phonetics("xqzptk")


def test_basic_analyze_runs(analyzer):
    analyzer.basic_analyze(")fnqkb4")
