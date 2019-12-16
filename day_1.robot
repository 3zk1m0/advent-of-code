*** Settings ***
Library     OperatingSystem
Library     String




*** Test Cases ***

Day 1 Part 1
    
    ${total}       Set Variable     0
    ${contents}    Get File         day_1.txt
    @{lines}       Split to lines   ${contents}
    :FOR  ${line}  IN  @{lines}
    \   ${value}    Convert To Integer  ${line}
    \   ${result}   Count fuel for Weight    ${line}
    \   ${total}    Evaluate    ${result} + ${total}
    log     ${total}

Day 1 Part 2
    ${total}       Set Variable     0
    ${contents}    Get File         day_1.txt
    @{lines}       Split to lines   ${contents}
    :FOR  ${line}  IN  @{lines}
    \   ${value}    Convert To Integer  ${line}
    \   ${result}   Count fuel for fuel    ${line}
    \   ${total}    Evaluate    ${result} + ${total}
    log     ${total}

*** Keywords ***

Count fuel for Weight
    [Arguments]     ${fuel}
    ${result}       Evaluate    (${fuel} / 3) - 2
    ${result}       Convert To Integer    ${result}
    Return From Keyword    ${result}

Count fuel for fuel
    [Arguments]     ${fuel}
    ${result}       Evaluate    ${fuel} / 3 - 2
    ${result}       Convert To Integer    ${result}
    ${test}         Evaluate    ${result} < 1
    Return From Keyword If  ${test}     0
    ${tmp}          Count fuel for fuel  ${result}
    ${result}       Evaluate    ${result} + ${tmp}
    Return From Keyword    ${result}
    
