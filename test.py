from faker import Faker
import random
import datetime

class TestData:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TestData, cls).__new__(cls)
            cls._instance.init_data()
        return cls._instance

    def init_data(self):
        # initiation
        self.auth_token = None
        self.resume_id = None
        self.full_resume = None
        self.other_data = {}

    def clear(self):
        # Очистка данных для завершения тестов
        self.init_data()


class ResumeData:
    def __init__(self):
        # Faker library initiation
        self.fake = Faker('en-US')
        self.data = self.generate_data()

    def generate_data(self):
        # Resume JSON generation
        return {
            "resume": {
                "contact": {
                    "firstName": self.fake.first_name(),
                    "lastName": self.fake.last_name(),
                    "email": self.fake.email(),
                    "phone": "+12055555555",
                    "state": self.fake.state(),
                    "country": self.fake.country(),
                    "linkedin": f"https://linkedin.com/in/{self.fake.user_name()}",
                    "website": self.fake.url()
                },
                "title": self.fake.job(),
                "summary": self.fake.text(max_nb_chars=150),
                "skills": ", ".join(self.fake.words(nb=6, unique=True)),
                "experience": [
                    self.generate_experience(),
                    self.generate_experience()
                ],
                "education": [
                    self.generate_education()
                ],
                "certifications": [
                    self.generate_certification(),
                    self.generate_certification()
                ]
            }
        }

    def generate_experience(self):
        # experience generation
        start_date = self.fake.date_between(start_date='-10y', end_date='-5y')
        end_date = self.fake.date_between(start_date='-4y', end_date='today')
        return {
            "id": str(random.randint(1, 100)),
            "jobTitle": self.fake.job(),
            "company": self.fake.company(),
            "startDate": start_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "endDate": end_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "location": self.fake.city(),
            "achievement": self.fake.text(max_nb_chars=100)
        }

    def generate_education(self):
        # Education generation
        start_date = self.fake.date_between(start_date='-15y', end_date='-10y')
        end_date = self.fake.date_between(start_date='-10y', end_date='-5y')
        return {
            "id": str(random.randint(1, 100)),
            "school": self.fake.company(),
            "degree": f"{self.fake.job()} Degree",
            "startDate": start_date.strftime("%Y-%m-%d"),
            "endDate": end_date.strftime("%Y-%m-%d"),
            "location": self.fake.city()
        }

    def generate_certification(self):
        # Cert generation
        return {
            "id": str(random.randint(1, 100)),
            "title": f"Certified {self.fake.job()} Specialist",
            "issuer": self.fake.company()
        }

    def get_data(self):
        return self.data


# Пример использования
if __name__ == '__main__':
    resume = ResumeData()
    print(resume.get_data())