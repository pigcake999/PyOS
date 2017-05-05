[BITS 16]
[org 0x7c00]

mov ah, 0x06
mov al, 0
int 10h
mov bx, string_ab
call print_string
mov bx, string_abc
call print_string
mov bx, string_abcd
call print_string

jmp $

print_string:
	pusha
	mov ah, 0x0e
print_loop:
	mov al, [bx]
	cmp al, 0
	je print_string_done
	int 0x10
	add bx, 1
	jmp print_loop
print_string_done:
	popa
	ret

string_ab db "Loading Christian OS...",0
string_abc db "",13,10,0
string_abcd db "Hello, World!",0


times 510 -($-$$) db 0
dw 0xaa55