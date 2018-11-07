from config import db, ma


class LabTest(db.Model):
    __tablename__ = 'lab_tests'
    test_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    unit = db.Column(db.String(32))
    value_min = db.Column(db.String(32))
    value_max = db.Column(db.String(32))
   

class LabTestSchema(ma.ModelSchema):
    class Meta:
        model = LabTest
        sqla_session = db.session
