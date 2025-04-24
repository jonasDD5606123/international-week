Feature: Drone- en startplaatsselectie voor reservering
  Scenario: Beschikbare drones tonen
    Given Een ingelogde piloot

    When De piloot vraagt de lijst van beschikbare drones en startplaatsen op

    Then Het systeem toont een lijst van drones en startplaatsen met hun beschikbaarheid

  Scenario: Drone reserveren
    Given Een ingelogde piloot en een beschikbare drone + startplaats

    When De piloot selecteert een drone en startplaats en bevestigt de reservatie

    Then Het systeem controleert beschikbaarheid en maakt een reservering aan