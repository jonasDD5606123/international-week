from behave import *

@given(u'Een nieuwe reservering is aangemaakt')
def step_impl(context, db):
    raise NotImplementedError('STEP: Given Een nieuwe reservering is aangemaakt')
    cursor = dbConn.cursor()
    cursor.execute('insert into reserveringen')
    

@when(u'Het systeem slaat de reservering op')
def step_impl(context, ):
    raise NotImplementedError(u'STEP: When Het systeem slaat de reservering op')


@then(u'De database bevat een record met piloot_id, drone_id, startplaats_id, reservatietijdstip, en status')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then De database bevat een record met piloot_id, drone_id, startplaats_id, reservatietijdstip, en status')


@given(u'Een piloot heeft een verslag ingediend')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given Een piloot heeft een verslag ingediend')


@when(u'Het systeem slaat het verslag op')
def step_impl(context):
    raise NotImplementedError(u'STEP: When Het systeem slaat het verslag op')


@then(u'De database bevat een record met verslaginhoud, timestamp, reservering_id, piloot_id, en optioneel beeldmateriaal')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then De database bevat een record met verslaginhoud, timestamp, reservering_id, piloot_id, en optioneel beeldmateriaal')