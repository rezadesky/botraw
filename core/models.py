from tortoise import Model, fields

class Teleport(Model):
    id = fields.IntField(pk=True)
    command = fields.CharField(max_length=50, unique=True)
    x = fields.FloatField()
    y = fields.FloatField()
    z = fields.FloatField()
    facing = fields.CharField(max_length=20, default="FrontRight")
    role = fields.CharField(max_length=50, default="public")

    class Meta:
        table = "teleports"

class Setting(Model):
    id = fields.IntField(pk=True)
    key = fields.CharField(max_length=50, unique=True)
    value = fields.TextField()

    class Meta:
        table = "settings"

class Role(Model):
    id = fields.IntField(pk=True)
    user_id = fields.CharField(max_length=255)
    username = fields.CharField(max_length=255, null=True)
    role_name = fields.CharField(max_length=50) # host, admin, vip, public

    class Meta:
        table = "roles"
        unique_together = (("user_id", "role_name"),)
