from pytest_bdd import given, when, then


@given(u'Een ingelogde piloot')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given Een ingelogde piloot')


@when(u'De piloot vraagt de lijst van beschikbare drones en startplaatsen op')
def step_impl(context):
    raise NotImplementedError(u'STEP: When De piloot vraagt de lijst van beschikbare drones en startplaatsen op')


@then(u'Het systeem toont een lijst van drones en startplaatsen met hun beschikbaarheid')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Het systeem toont een lijst van drones en startplaatsen met hun beschikbaarheid')


@given(u'Een ingelogde piloot en een beschikbare drone + startplaats')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given Een ingelogde piloot en een beschikbare drone + startplaats')


@when(u'De piloot selecteert een drone en startplaats en bevestigt de reservatie')
def step_impl(context):
    raise NotImplementedError(u'STEP: When De piloot selecteert een drone en startplaats en bevestigt de reservatie')


@then(u'Het systeem controleert beschikbaarheid en maakt een reservering aan')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Het systeem controleert beschikbaarheid en maakt een reservering aan')