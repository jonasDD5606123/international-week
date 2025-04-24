Feature: Verslaglegging na drone-inzet
  Scenario: Verslag succesvol indienen
    Given Een ingelogde piloot met een actieve reservering en een verslag

    When De piloot vult het verslagformulier in en dient het in

    Then Het systeem koppelt het verslag aan de reservering en zet de drone terug op "beschikbaar"

  Scenario: Verslag zonder verplichte velden
    Given Een ingelogde piloot met een actieve reservering

    When De piloot probeert een verslag in te dienen zonder "incidentinhoud"

    Then Het systeem weigert het verslag en vraagt om verplichte velden in te vullen