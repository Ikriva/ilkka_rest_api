from flask import make_response, abort
from config import db
from models import LabTest, LabTestSchema


# Create a handler for our read (GET) labTests
def read():
    """
    This function responds to a request for /api/labTests
    with the complete lists of labTests

    :return:        sorted list of labTests
    """
    # Create the list of labTests from our data
    labTest = LabTest.query \
        .order_by(LabTest.test_id) \
        .all()

    # Serialize the data for the response
    labTest_schema = LabTestSchema(many=True)
    return labTest_schema.dump(labTest).data


def read_one(test_id):
    """
    This function responds to a request for /api/labTests/{test_id}
    with one matching laboratory test from database

    :param test_id:   ID of labTest to find
    :return:            labTest matching ID
    """
    # Get the labTest requested
    labTest = LabTest.query \
        .filter(LabTest.test_id == test_id) \
        .one_or_none()

    if labTest is not None:
        # Serialize the data for the response
        labTest_schema = LabTestSchema()
        return labTest_schema.dump(labTest).data

    else:
        abort(404, 'LabTest not found for Id: {labTest_id}'.format(labTest_id=test_id))


def create(labTest):
    """
    This function creates a new laboratory test 
    based on the passed-in laboratory test data

    :param labTest:  labTest to create in labTests structure
    :return:         201 on success, 406 on laboratory test exists
    """
    name = labTest.get('name')
    test_id = labTest.get('test_id')

    # Checking only for id
    existing_labTest = LabTest.query \
        .filter(LabTest.test_id == test_id) \
        .one_or_none()

    # existing_labTest = LabTest.query \
    #    .filter(or_(LabTest.name == name, LabTest.test_id == test_id)) \
    #    .one_or_none()

    if existing_labTest is None:
        schema = LabTestSchema()
        new_labTest = schema.load(labTest, session=db.session).data

        db.session.add(new_labTest)
        db.session.commit()

        # Serialize and return the newly created labTest in the response
        return schema.dump(new_labTest).data, 201

    else:
        abort(409, f'Laboratory test with name {name} or test_id exists already')


def update(test_id, labTest):
    """
    This function updates an existing labTest in the labTests structure
    :param test_id:          Id of the labTest to update in the labTests structure
    :param labTest:      labTest to update
    :return:            updated labTest structure
    """
    # Get the labTest requested from the db into session
    update_labTest = LabTest.query.filter(
        LabTest.test_id == test_id
        ).one_or_none()

    # Did we find a labTest?
    if update_labTest is not None:

        # turn the passed in labTest into a db object
        schema = LabTestSchema()
        updated = schema.load(labTest, session=db.session).data

        # Set the id to the labTest we want to update
        updated.test_id = update_labTest.test_id

        # merge the new object into the old and commit it to the db
        db.session.merge(updated)
        db.session.commit()

        # return updated labTest in the response
        data = schema.dump(update_labTest).data

        return data, 200

    # Otherwise, nope, didn't find that labTest
    else:
        abort(
            404,
            "Lab test not found for Id: {id}".format(id=id),
        )


def delete(test_id):
    """
    This function deletes a labTest from the labTests structure
    :param test_id:   Id of the labTest to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the labTest requested
    labTest = LabTest.query.filter(LabTest.test_id == test_id).one_or_none()

    # Did we find a labTest?
    if labTest is not None:
        db.session.delete(labTest)
        db.session.commit()
        return make_response(
            "Laboratory test {test_id} {name} deleted".format(test_id=test_id, name=labTest.name), 200
        )

    # Otherwise, nope, didn't find that labTest
    else:
        abort(
            404,
            "Laboratory test not found for Id: {test_id}".format(test_id=test_id),
        )


