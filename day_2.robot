*** Settings ***
Library     OperatingSystem
Library     String
Library     Collections




*** Test Cases ***

Day 1 Part 1
    
    ${contents}    Get File         day_2.txt
    @{state}       Split String   ${contents}   ,
    Set List Value      ${state}    1   12
    Set List Value      ${state}    2   2
    Set Test Variable   @{state}
    Set Test Variable   ${pointer}      0
    ${length}   Get length  ${state}
    ${length}      Evaluate    ${length}-1
    :FOR  ${code}  IN RANGE  0  ${length}   4
    \    Set Test Variable   ${pointer}     ${code}
    \   Operate OP Code
    log     @{state}[0]


Day 1 Part 2
    Set Test Variable   ${the_noun}     0
    Set Test Variable   ${the_verb}     0
    For Noun
    ${result}   Evaluate    100 * ${the_noun} + ${the_verb}
    log     ${result}

*** Keywords ***

For Noun

    :FOR    ${noun}  IN RANGE  0  100   # takes 80min from 0, set to start from 80
    \   ${result}   For Verb    ${noun}
    \   Return From Keyword If   ${result}


For Verb
    [Arguments]     ${noun}
    :FOR    ${verb}  IN RANGE  0  100
    \   log to console  ${noun} - ${verb}
    \   Run Int Code Computer     ${noun}     ${verb}
    \   Set Test Variable   ${the_verb}     ${verb}
    \   Set Test Variable   ${the_noun}     ${noun}
    \   ${result}   Get From List   ${state}    0
    \   Return From Keyword If      ${result}==19690720      ${True}

Run Int Code Computer
    [Arguments]     ${noun}     ${verb}
    ${contents}    Get File         day_2.txt
    @{state}       Split String   ${contents}   ,
    Set List Value      ${state}    1   ${noun}
    Set List Value      ${state}    2   ${verb}
    Set Test Variable   @{state}
    Set Test Variable   ${pointer}      0
    ${length}   Get length  ${state}
    ${length}      Evaluate    ${length}-1
    :FOR  ${code}  IN RANGE  0  ${length}   4
    \    Set Test Variable   ${pointer}     ${code}
    \   Operate OP Code
    log     @{state}[0]

Operate OP Code
    log     ${pointer}
    ${opcode}   Get From List   ${state}    ${pointer}
    Run Keyword If  ${opcode}==1    OP Addition
    Run Keyword If  ${opcode}==2    OP Multiplication
    Run Keyword If  ${opcode}==99    Return From Keyword    ${True}
    log     ${state}

OP Addition
    ${pt1}      Evaluate    ${pointer}+1
    ${pt2}      Evaluate    ${pointer}+2
    ${pt3}      Evaluate    ${pointer}+3
    ${param1}   Get From List   ${state}    ${pt1}
    ${param2}   Get From List   ${state}    ${pt2}
    ${param3}   Get From List   ${state}    ${pt3}
    ${param1}   Get From List   ${state}    ${param1}
    ${param2}   Get From List   ${state}    ${param2}
    ${result}      Evaluate    ${param1} + ${param2}
    Set List Value      ${state}    ${param3}  ${result}


OP Multiplication
    ${pt1}      Evaluate    ${pointer}+1
    ${pt2}      Evaluate    ${pointer}+2
    ${pt3}      Evaluate    ${pointer}+3
    ${param1}   Get From List   ${state}    ${pt1}
    ${param2}   Get From List   ${state}    ${pt2}
    ${param3}   Get From List   ${state}    ${pt3}
    ${param1}   Get From List   ${state}    ${param1}
    ${param2}   Get From List   ${state}    ${param2}
    ${result}      Evaluate    ${param1} * ${param2}
    Set List Value      ${state}    ${param3}  ${result}