##[Crypto 150] Bomba

This challenge is supposed to be an easy crypto challenge maybe 100 to 150
I used py-enigma library to emulate an enigma machine.

I included the python script which can break the encrypted text. 


#### To include to the challenger: 
Sheet.png

##### this is the encrypted text they must break
VJTLWDQYBJMSAMURBOQXYSBZEYNRLGRNKKVQYJKEKRGMSCYBMH

##### this is the plain text message
DAMNXTHATXBOMBAXKRYPTOLOGICZNAXANDXMARIANXREJEWSKI

Also included should be a small text saying that 
the script should be inserted inbetween curly brackets of sun{} 

##### This is my python script to test
from enigma.machine import EnigmaMachine

###### setup machine according to specs from a daily key sheet:

machine = EnigmaMachine.from_key_sheet(
       rotors='V I IV',
       reflector='B',
       ring_settings=[18, 11, 25],
       plugboard_settings='TS IK AV QP HW FM DX NG CY UE')

###### set machine initial rotor starting position
machine.set_display('MHW')

###### decrypt the message key
enc_key = machine.process_text('LWB')

print( enc_key + "\n")

###### decrypt the cipher text with the unencrypted message key
machine.set_display('LWB')

ciphertext = 'DAMNXTHATXBOMBAXKRYPTOLOGICZNAXANDXMARIANXREJEWSKI'
plaintext = machine.process_text(ciphertext)

print(plaintext)

machine.set_display('MHW')
msg_key = machine.process_text('FLC')
machine.set_display(msg_key)

print('\n' + msg_key + '\n')

plain2 = machine.process_text(plaintext)
print('')
print(plain2)
