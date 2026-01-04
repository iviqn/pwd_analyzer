import json
import os
import requests
import random
import string
import hashlib

class PasswordAnalyzer:
    
    def __init__(self, history_file='password_history.json', 
                 rockyou_file='rockyou.txt'):
        self.history_file = history_file
        if rockyou_file:
            self.rockyou_file = self.load_rockyou()
        else:
            self.rockyou_file = set()             
        self.HIBP_API_URL = "https://api.pwnedpasswords.com/range/"
        self.rockyou_passwords = self.load_rockyou()
        self.top_100_passwords = self.load_top()
    
    def load_rockyou(self):
        rockyou_pass = set()
        with open(self.rockyou_file, 'r', encoding='utf-8', 
                errors='ignore') as f:
            for i in f:
                if i.strip():
                    rockyou_pass.add(i.strip())
        return rockyou_pass
    def load_top(self):
        return [
            "123456", "password", "12345678", "qwerty", "123456789", "12345", 
            "1234", "111111", "1234567", "dragon", "123123", "baseball", 
            "abc123", "football", "monkey", "letmein", "696969", "shadow",
            "master", "666666", "qwertyuiop", "123321", "mustang", "1234567890",
            "michael", "654321", "pussy", "superman", "1qaz2wsx", "7777777",
            "fuckyou", "121212", "000000", "qazwsx", "123qwe", "killer",
            "sunshine", "iloveyou", "fuckme", "2000", "charlie", "robert",
            "thomas", "hockey", "ranger", "daniel", "starwars", "klaster",
            "112233", "george", "asshole", "computer", "michelle", "jessica",
            "pepper", "1111", "zxcvbn", "555555", "11111111", "131313",
            "freedom", "777777", "pass", "fuck", "maggie", "13579",
            "summer", "love", "ashley", "6969", "nicole", "chelsea",
            "william", "matthew", "access", "yankees", "987654321"
        ]
    
    def gen_pass(self):
        while True:
            size = int(input("Длина пароля (8-16): "))
            if 8<=size<=16:
                break
        print("")
        print("Тип генерации:")
        print("1) Все символы (цифры+буквы+спец)")
        print("2) Буквы+цифры или буквы+спец")
        print("3) По маске (d=цифра, l=буква, s=спецсимвол)")
        
        choice = input("Выберите (1-3): ")
        if choice=="1":
            return self.gen_all(size)
        elif choice=="2":
            return self.gen_mix(size)
        elif choice=="3":
            return self.gen_mask()
        else:
            return self.gen_all(size)
    
    def gen_all(self, size):
        lwr = "abcdefghijklmnopqrstuvwxyz"
        upr = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        dig = "0123456789"
        sym = "!@#$%^&*_-"
        all_chars = lwr+upr+dig+sym
        pwd = [
            random.choice(lwr),
            random.choice(upr),
            random.choice(dig),
            random.choice(sym)
        ]
        for i in range(size-4):
            pwd.append(random.choice(all_chars))
        
        random.shuffle(pwd)
        return ''.join(pwd)
    
    def gen_mix(self, size):
        print("\n1) Буквы+цифры")
        print("2) Буквы+спецсимволы")
        ch = input("Выберите (1-2): ")
        letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if ch == "1":
            dig = "0123456789"
            all_chars = letters+dig
            pwd = [random.choice(letters), random.choice(dig)]
        else:
            sym = "!@#$%^&*_-"
            all_chars = letters+sym
            pwd = [random.choice(letters), random.choice(sym)]
        for i in range(size-2):
            pwd.append(random.choice(all_chars))
        random.shuffle(pwd)
        return ''.join(pwd)
    
    def gen_mask(self):
        mask = input("Маска (d=цифра, l=буква, s=спец): ")
        lwr = "abcdefghijklmnopqrstuvwxyz"
        upr = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        dig = "0123456789"
        sym = "!@#$%^&*_-"
        
        p = []
        for i in mask:
            if i=='d':
                p.append(random.choice(dig))
            elif i=='l':
                p.append(random.choice(lwr + upr))
            elif i=='s':
                p.append(random.choice(sym))
            else:
                p.append(random.choice(lwr+upr+dig+sym))
        
        return ''.join(p)
    
    def leaks(self, password):
        if password in self.rockyou_passwords:
            return True
        return False
    
    def check_hibp(self, password):
        sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
        first5 = sha1_hash[:5]
        ost = sha1_hash[5:]
        resp = requests.get(f"https://api.pwnedpasswords.com/range/{first5}")
        for i in resp.text.splitlines():
            if i.startswith(ost):
                parts = i.split(':')
                return {
                    'found': True,
                    'msg': 'Найден в утечках',
                }
        
        return {
            'found': False,
            'msg': 'Не найден в утечках',
        }
    
    def pops(self, password):
        pwd_lower = password.lower()
        exact = pwd_lower in self.top_100_passwords
        similar = []
        for i in self.top_100_passwords:
            if (i in pwd_lower or pwd_lower in i):
                similar.append(i)
        
        return {
            'exact': exact,
            'similar': similar[:3],
            'score': len(similar)
        }
    
    def phonetics(self, password):
        gl = set('aeiouy')
        sgl = set('bcdfghjklmnpqrstvwxz')
        glcount, sglcount = 0,0
        for char in password.lower():
            if char in gl:
                glcount+=1
            elif char in sgl:
                sglcount+=1
        rating = glcount/(glcount_sglcount)
        if rating<0.2 or rating>0.8:
            comfort = 'сложно произнести'
        else:
            comfort = 'легко произнести'
        
        return {
            'comfort': comfort,
            'rating': round(rating, 2)
        }
    
    def has_digits(self, password):
        for i in password:
            if i.isdigit():
                return True
        return False
    def has_upper(self, password):
        for i in password:
            if i.isupper():
                return True
        return False
    def has_lower(self, password):
        for i in password:
            if i.islower():
                return True
        return False
    def has_special(self, password):
        specials = "!@#$%^&*()_+-=[]{;:,.<>/?"
        for i in password:
            if i in specials:
                return True
        return False
    def has_repeat(self, password):
        if len(password)>=3:
            for i in range(len(password)-2):
                if password[i]==password[i+1]==password[i+2]:
                    return True
        seqs = ['abc', 'qwe', 'xyz', '123', '234', '345', '456', '789', '012']
        for i in seqs:
            if i in password.lower():
                return True
        return False
    def has_common_pattern(self, password):
        patterns = [
            'qwerty','asdfgh', 'zxcvbn',
            '123456', '654321', '112233', '223344', 'password', 'admin',
            'login', 'welcome', 'secret'
        ]
        for i in patterns:
            if i in password.lower():
                return True
        
        return False
    
    def basic_analyze(self, password):
        scan_res = {
            'has_digits': self.has_digits(password),
            'has_upper': self.has_upper(password),
            'has_lower': self.has_lower(password),
            'has_special': self.has_special(password),
            'has_repeats': self.has_repeat(password),
            'has_common_pattern': self.has_common_pattern(password),
            'size': len(password),
            'unique_chars': len(set(password))
        }
        
        rating = self.basic_rating(password)
        recs = self.basic_recs(scan_res)
        
        return {
            'password': password,
            'rating': rating,
            'level': self.basic_level(rating),
            'scan_res': scan_res,
            'recs': recs,
            'analysis_type': 'BASIC',
            'leak_check': False,
            'phonetic_check': False,
            'hibp_check': False
        }
    
    def leak_analyze(self, password):
        leak = self.leaks(password)
        pop = self.pops(password)
        hibp_res = self.check_hibp(password)

        if leak or hibp_res['found']:
            level = 'найден в утечках'
            recs = ['Замените пароль']
        else:
            level = 'не найден'
            recs = ['Пароль не найден в утечках']

        return {
            'password': password,
            'leak': leak,
            'pop': pop,
            'hibp': hibp_res,
            'level': level,
            'recs': recs,
            'analysis_type': 'LEAK_CHECK',
            'basic_criteria': False,
            'phonetic_check': False,
            'hibp_check': True
        }
    def all_analyze(self, password):
        leak = self.leaks(password)
        pop = self.pops(password)
        phonetic = self.phonetics(password)
        hibp_res = self.check_hibp(password) 
        scan_res = {
            'has_digits': self.has_digits(password),
            'has_upper': self.has_upper(password),
            'has_lower': self.has_lower(password),
            'has_special': self.has_special(password),
            'has_repeats': self.has_repeat(password),
            'has_common_pattern': self.has_common_pattern(password),
            'size': len(password),
            'unique_chars': len(set(password))
        }
        rating = self.comp_rating(password, leak, hibp_res)
        recs = self.comp_recs(scan_res, leak, pop, phonetic, hibp_res)
        return {
            'password': password,
            'rating': rating,
            'level': self.comp_level(rating, leak, hibp_res),
            'leak': leak,
            'pop': pop,
            'phonetic': phonetic,
            'hibp': hibp_res,
            'scan_res': scan_res,
            'recs': recs,
            'analysis_type': 'comprehensive',
            'basic_criteria': True,
            'leak_check': True,
            'phonetic_check': True,
            'hibp_check': True
        }
    
    def basic_rating(self, password):
        rating = 0
        size = len(password)
        if size>=13:
            rating+=5
        elif size>=10:
            rating+=4
        elif size>=8:
            rating+=3
        elif size>=6:
            rating+=2
        elif size>=4:
            rating+=1
        char_types = 0
        if self.has_digits(password):
            char_types+=1
        if self.has_upper(password):
            char_types+=1
        if self.has_lower(password):
            char_types+=1
        if self.has_special(password):
            char_types+=1
        if char_types==4:
            rating+=3
        elif char_types==3:
            rating+=2
        elif char_types==2:
            rating+=1
        if len(set(password))>=size*0.8:
            rating += 2
        if self.has_repeat(password):
            rating-=2
        if self.has_common_pattern(password):
            rating-=2
        if size>=12 and not self.has_repeat(password) and not self.has_common_pattern(password):
            if len(set(password)) >= size * 0.7:
                rating += 2
        
        return max(1, min(10, rating))
    
    def comp_rating(self, password, leak, hibp_res):
        rating = self.basic_rating(password)
        
        if leak:
            rating = max(1, rating-3)
        
        if hibp_res['found']:
            if hibp_res['leak_count']>100:
                rating = max(1, rating-4)
            elif hibp_res['leak_count']>10:
                rating = max(1, rating-3)
            elif hibp_res['leak_count']>0:
                rating = max(1, rating-2)
        return max(1, min(10, rating))
    
    def basic_level(self, rating):
        if rating>=9:
            return "Отличный"
        elif rating>=7:
            return "Хороший"
        elif rating>=5:
            return "Средний"
        elif rating>=3:
            return "Плохой"
        else:
            return "Очень слабый"
    
    def comp_level(self, rating, leak, hibp_res):
        if leak or hibp_res['found']:
            return "Найден в утечках"
        else:
            return self.basic_level(rating)
    
    def basic_recs(self, scan):
        recs = []
        if not scan['has_digits']:
            recs.append("Добавьте цифры")
        if not scan['has_upper']:
            recs.append("Добавьте заглавные буквы")
        if not scan['has_lower']:
            recs.append("Добавьте строчные буквы")
        if not scan['has_special']:
            recs.append("Добавьте спецсимволы")
        if scan['has_repeats']:
            recs.append("Избегайте повторов символов и последовательностей")
        if scan['has_common_pattern']:
            recs.append("Избегайте распространенных паттернов")
        if scan['size']<8:
            recs.append("Увеличьте длину до 8 или более знаков")
        elif scan['size']<10:
            recs.append("Рекомендуется длина 10+ символов")
        return recs
    
    def comp_recs(self, scan, leak, pop, phonetic, hibp_res):
        recs = self.basic_recs(scan)
        if pop['exact']:
            recs.append("Пароль найден в топ-100 популярных паролей")
        elif pop['score']>0:
            recs.append(f"Пароль похож на популярные: {', '.join(pop['similar'])}")
        if leak:
            recs.insert(0, "Пароль найден в локальной базе утечек")
        if hibp_res['found']:
            recs.insert(0, f"Пароль найден в утечках через HIBP")
        if phonetic['comfort']=='сложно произнести':
            recs.append("Пароль сложно произнести")
        return recs
    
    def batch_analyze(self, passwords, analysis_type='comprehensive'):
        ans = {}
        for i in passwords:
            if analysis_type=='basic':
                ans[i] = self.basic_analyze(i)
            elif analysis_type=='leak':
                ans[i] = self.leak_analyze(i)
            else:  
                ans[i] = self.all_analyze(i)
        return ans
