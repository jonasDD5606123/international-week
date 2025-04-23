Feature: Beschikbaarheidscontrole en reservatie
  Scenario: Drone niet beschikbaar
    Given Een ingelogde piloot die een drone wil reserveren

    When De geselecteerde drone is al gereserveerd op het gewenste moment

    Then Het systeem toont een foutmelding en vraagt een nieuwe selectie

#Scenario: Succesvolle reservatie
#    Given Een ingelogde piloot en een beschikbare drone + startplaats
#
#    When De piloot bevestigt de reservatie
#
#    Then Het systeem markeert de drone en startplaats als "gereserveerd" en slaat de reservatie op