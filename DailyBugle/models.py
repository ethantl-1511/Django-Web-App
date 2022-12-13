from django.db import models

# Choices for PeopleOfInternet model
TYPE_CHOICES = {
    ('alive','alive'),
    ('dead','dead'),
    ('missing','missing'),
    ('unknown','unknown'),
}

# Model for tracking possible Spider-People
class PeopleOfInterest(models.Model):
    # which Spider-Person are they?
    alias = models.CharField(max_length=50, default="", blank=False, null=False)
    # suspected real name
    real_name = models.CharField(max_length=50, default="unknown", blank=True, null=False)
    # dead or alive?
    status = models.CharField(max_length=50, choices=TYPE_CHOICES)
    # reporter can name themselves or be left Anonymous
    reporter = models.CharField(max_length=50, default="anonymous", blank=True)
    # optional description of the Spider-Person
    description = models.TextField(max_length=255, default="", blank=True)

    people = models.Manager()

    def __str__(self):
        return self.alias

# Model for saving random facts
class RandomFact(models.Model):
    random_fact = models.TextField(max_length=500, default="", blank=False, null=False)
    fact_source = models.TextField(max_length=50, default="", blank=False, null=False)

    facts = models.Manager()

    def __str__(self):
        return self.random_fact