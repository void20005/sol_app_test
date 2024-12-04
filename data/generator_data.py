import allure
from faker import Faker
import random
import string
import datetime


def generate_us_phone_with_faker():
    fake = Faker('en_US')
    raw_number = fake.msisdn()
    return f"+1{raw_number[-10:]}"


class GeneratorData:
    def __init__(self):
        """
        Initialize the generator with the specified mode.
        :param mode: "faker" for quick data generation, "manual" for validation testing.
        """
        self.fake = Faker()
        self.resume_valid_ids = []
        self.base_resume_valid_ids = []
        self.DATA_TYPES = {
            'lowercase': string.ascii_lowercase,  # Lowercase Latin letters
            'uppercase': string.ascii_uppercase,  # Uppercase Latin letters
            'latin': string.ascii_letters,  # Latin letters (both cases) + space
            'spec': '!@#$%^&*()[]{};:<>?/+=_-',  # Special characters
            'digits': string.digits,  # Digits 0-9
            'alphanumeric': string.ascii_letters + string.digits,  # Latin letters + digits
            'whitespace': ' \t\n',  # Whitespaces, tabs, and newlines
            'unicode_emoji': '😀😃😄😁😆😅😂🤣😊😇😉😍😘',  # Popular emoji characters
            'diacritics': 'ąćęłńóśźżĄĆĘŁŃÓŚŹŻàèìòùÀÈÌÒÙáéíóúÁÉÍÓÚäëïöüÄËÏÖÜçÇÿŸ'  # Latin letters with diacritics
        }



    @staticmethod
    def merge_with_defaults(defaults, overrides):
            """
            Merge user-defined values with default values.

            :param defaults: Dictionary of default values.
            :param overrides: Dictionary of user-defined values.
            :return: Merged dictionary.
            """
            result = defaults.copy()
            result.update(overrides)
            return result


    def generate_random_string(self, length=10, data_types=None, additional_chars=''):
        """
        Generate a random string from multiple data types.

        :param length: Length of the string to generate.
        :param data_types: List of keys in DATA_TYPES to combine. e.g. [latin] or [latin, spec]
        :param additional_chars: Additional characters to include.
        :return: Generated string.
        """
        if not data_types:
            data_types = ['latin']  # Default to latin if no types specified
        # Combine character sets from all specified data types
        char_set = ''.join(self.DATA_TYPES[data_type] for data_type in data_types if data_type in self.DATA_TYPES)
        char_set += additional_chars

        if not char_set:
            raise ValueError(f"No valid character sets found for data_types: {data_types}")
        return ''.join(random.choice(char_set) for _ in range(length))



    @allure.step("Generate invalid resume ID")
    def generate_resume_invalid_id(self, overrides=None):
        """
        Generate an invalid resume ID with customizable parameters.

        :param overrides: Dictionary of overrides for customization.
            - length: Length of the string (default: 10).
            - data_types: List of character types (default: ['spec']).
            - additional_chars: Additional characters to include (default: '!@#$').
        :return: Generated invalid resume ID.
        """
        # Default parameters for generating an invalid ID
        defaults = {
            "length": 10,
            "data_types": ['spec'],  # Use special characters by default
            "additional_chars": ''  # Add extra special characters
        }
        # Merge defaults with overrides
        params = self.merge_with_defaults(defaults, overrides or {})
        # Generate the invalid ID
        return self.generate_random_string(
            length=params["length"],
            data_types=params["data_types"],
            additional_chars=params["additional_chars"])



    @allure.step("Generate US phone")
    def generate_valid_us_phone_number(self):
        country_code = "+1"
        area_code = f"{random.randint(2, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
        central_office_code = f"{random.randint(2, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
        line_number = f"{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}{random.randint(0, 9)}"
        phone_number = f"{country_code}{area_code}{central_office_code}{line_number}"
        return phone_number



    @allure.step("Generate some non existent resume id")
    def generate_resume_non_existent_id(self):
        return random.randint(10**10, 10**11 - 1)



    @allure.step("Generate job descriptions")
    def generate_job_description(self, qty):
        result = []
        for i in range(qty):
            result.append(self.fake.job())
        return result

    def generate_resume_name(self):
        return  self.fake.name()

    @allure.step("Generate a resume (JSON)")
    def generate_resume(self, overrides=None):
        """
        Generate a complete resume JSON structure.

        :param overrides: Dictionary of overrides for specific fields or sections.
            - contact: Custom values for the contact section.
            - title: Custom job title.
            - summary: Custom summary text.
            - skills: Custom skills string.
            - experience: List of custom experiences.
            - education: List of custom educations.
            - certifications: List of custom certifications.
        :return: A JSON object representing the resume.
        """
        # Default resume structure
        defaults = {
            "contact": {
                "firstName": self.fake.first_name(),
                "lastName": self.fake.last_name(),
                "email": self.fake.email(),
                "phone": self.generate_valid_us_phone_number(),
                "state": self.fake.state(),
                "country": self.fake.country(),
                "linkedin": f"https://linkedin.com/in/{self.fake.user_name()}",
                "website": self.fake.url()
            },
            "title": self.fake.job(),
            "summary": self.fake.text(max_nb_chars=150),
            "skills": ", ".join(self.fake.words(nb=6, unique=True)),
            "experience": [self.generate_experience() for _ in range(2)],
            "education": [self.generate_education()],
            "certifications": [self.generate_certification() for _ in range(2)]
        }

        # Merge defaults with overrides
        resume_data = self.merge_with_defaults(defaults, overrides or {})
        return resume_data

    def generate_experience(self, overrides=None):
        """
        Generate a single experience entry.
        :param overrides: Custom values for experience fields.
        :return: A dictionary representing an experience.
        """
        defaults = {
            "id": str(random.randint(1, 100)),
            "jobTitle": self.fake.job(),
            "company": self.fake.company(),
            "startDate": self.fake.date_between(start_date='-10y', end_date='-5y').strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "endDate": self.fake.date_between(start_date='-4y', end_date='today').strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "location": self.fake.city(),
            "achievement": self.fake.text(max_nb_chars=100)
        }
        return self.merge_with_defaults(defaults, overrides or {})

    def generate_education(self, overrides=None):
        """
        Generate a single education entry.
        :param overrides: Custom values for education fields.
        :return: A dictionary representing education.
        """
        defaults = {
            "id": str(random.randint(1, 100)),
            "school": self.fake.company(),
            "degree": f"{self.fake.job()} Degree",
            "startDate": self.fake.date_between(start_date='-15y', end_date='-10y').strftime("%Y-%m-%d"),
            "endDate": self.fake.date_between(start_date='-10y', end_date='-5y').strftime("%Y-%m-%d"),
            "location": self.fake.city()
        }
        return self.merge_with_defaults(defaults, overrides or {})

    def generate_certification(self, overrides=None):
        """
        Generate a single certification entry.
        :param overrides: Custom values for certification fields.
        :return: A dictionary representing a certification.
        """
        defaults = {
            "id": str(random.randint(1, 100)),
            "title": f"Certified {self.fake.job()} Specialist",
            "issuer": self.fake.company()
        }
        return self.merge_with_defaults(defaults, overrides or {})
########Example of overriding call the generate_resume() function#################################
##      custom_resume = generator_data.generate_resume({                                        ##
##          "contact": {"firstName": "John", "lastName": "Doe"},                                ##
##          "experience": [generator_data.generate_experience({"jobTitle": "Custom Job"})],     ##
##          "title": "Custom Title"                                                             ##
##      })                                                                                      ##
##################################################################################################