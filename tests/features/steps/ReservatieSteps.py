from pytest_bdd import given, when, then


@given(u'Een ingelogde piloot die een drone wil reserveren')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given Een ingelogde piloot die een drone wil reserveren')


@when(u'De geselecteerde drone is al gereserveerd op het gewenste moment')
def step_impl(context):
    raise NotImplementedError(u'STEP: When De geselecteerde drone is al gereserveerd op het gewenste moment')


@then(u'Het systeem toont een foutmelding en vraagt een nieuwe selectie')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Het systeem toont een foutmelding en vraagt een nieuwe selectie')