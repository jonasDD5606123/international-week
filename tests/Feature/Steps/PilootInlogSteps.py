from pytest_bdd import given, when, then


@given(u'Een geregistreerde piloot met geldige inloggegevens')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given Een geregistreerde piloot met geldige inloggegevens')


@when(u'De piloot vult zijn/haar credentials in en klikt op "Aanmelden"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When De piloot vult zijn/haar credentials in en klikt op "Aanmelden"')


@then(u'Het systeem verleent toegang en toont het dashboard')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Het systeem verleent toegang en toont het dashboard')


@given(u'Een geregistreerde piloot met ongeldige inloggegevens')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given Een geregistreerde piloot met ongeldige inloggegevens')


@when(u'De piloot vult een verkeerd wachtwoord in en klikt op "Aanmelden"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When De piloot vult een verkeerd wachtwoord in en klikt op "Aanmelden"')


@then(u'Het systeem toont een foutmelding en blokkeert toegang')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then Het systeem toont een foutmelding en blokkeert toegang')
