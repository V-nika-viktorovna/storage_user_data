from tortoise import Model, fields
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):

    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=100, null=True)
    last_name = fields.CharField(max_length=100, null=True)
    other_name = fields.CharField(max_length=100, null=True)
    email = fields.CharField(max_length=100, unique=True)
    phone = fields.CharField(max_length=20, null=True)
    birthday = fields.DateField(null=True)
    city = fields.IntField(max_length=100, null=True)
    additional_info = fields.TextField(null=True)
    is_admin = fields.BooleanField(default=False)
    password_hash = fields.CharField(max_length=128, null=True)

    class Meta:
        table = "users"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

#
# class City(Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=100)
#
#     def __str__(self):
#         return self.id


User_Pydantic = pydantic_model_creator(User, name="User")
UserIn_Pydantic = pydantic_model_creator(User, name="UserIn", exclude_readonly=True)
# City_Pydantic = pydantic_model_creator(City, name="City")
# CityIn_Pydantic = pydantic_model_creator(City, name="CityIn", exclude_readonly=True)
