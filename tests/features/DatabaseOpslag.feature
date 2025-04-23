Feature: Datastructuur en opslag van reserveringen & verslagen
  Scenario: Reservatie opslaan
    Given Een nieuwe reservering is aangemaakt

    When Het systeem slaat de reservering op

    Then De database bevat een record met piloot_id, drone_id, startplaats_id, reservatietijdstip, en status

  Scenario: Verslag opslaan
    Given Een piloot heeft een verslag ingediend

    When Het systeem slaat het verslag op

    Then De database bevat een record met verslaginhoud, timestamp, reservering_id, piloot_id, en optioneel beeldmateriaal