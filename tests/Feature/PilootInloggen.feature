Feature: Piloot authenticatie en inlog proces
  Scenario: Succesvol inloggen
    Given Een geregistreerde piloot met geldige inloggegevens

    When De piloot vult zijn/haar credentials in en klikt op "Aanmelden"

    Then Het systeem verleent toegang en toont het dashboard

Scenario: Onsuccesvol inloggen (verkeerd wachtwoord)
    Given Een geregistreerde piloot met ongeldige inloggegevens

    When De piloot vult een verkeerd wachtwoord in en klikt op "Aanmelden"

    Then Het systeem toont een foutmelding en blokkeert toegang