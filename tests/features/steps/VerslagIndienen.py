from behave import *

@given(u'Een ingelogde piloot met een actieve reservering')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given Een ingelogde piloot met een actieve reservering')


@when(u'De piloot vult het verslagformulier in (met observaties en optionele afbeelding) en dient het in')
def step_impl(context):
    raise NotImplementedError(u'STEP: When De piloot vult het verslagformulier in (met observaties en optionele afbeelding) en dient het in')


@then(u'Het systeem koppelt het verslag aan de reservering en zet de drone terug op "beschikbaar"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Het systeem koppelt het verslag aan de reservering en zet de drone terug op "beschikbaar"')


@when(u'De piloot probeert een verslag in te dienen zonder "incidentinhoud"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When De piloot probeert een verslag in te dienen zonder "incidentinhoud"')


@then(u'Het systeem weigert het verslag en vraagt om verplichte velden in te vullen')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Het systeem weigert het verslag en vraagt om verplichte velden in te vullen')