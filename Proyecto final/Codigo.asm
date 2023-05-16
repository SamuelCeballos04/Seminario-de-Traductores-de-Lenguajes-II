section .data
		primr: db "El resultado es:= %lf", 10,0
section .bss
		resp: resq 3
section .text
extern printf

global multiplicacion
, main

multiplicacion:
		PUSH rbp
		MOV rbp, rsp
		SUB rsp, 48
MOV QWORD [rbp -24], rdi

MOV QWORD [rbp -28], rsi

		MOV rax, QWORD [rbp -28]

		MOV rdi, QWORD [rbp -24]

		ADD rax, rdi

		ADD rsp, 48
		MOV rsp, rbp
		POP rbp
		ret

main: 
		PUSH rbp
		MOV rbp, rsp
		SUB rsp, 48
		MOV WORD [rbp -4] , 8
		MOV WORD [rbp -8] , 4
		MOV rax, QWORD [rbp -4]
		MOV rdi, rax
		MOV rax, QWORD [rbp -8]
		MOV rsi, rax

		call multiplicacion

		MOV QWORD [rbp -8], rax
		PUSH QWORD [rbp -8]
		FILD DWORD [rsp]
		FILD QWORD [rel resp]
		ADD rsp, 8
		MOVSD xmm0, QWORD [rel resp]
		MOD rdi, primr
		mov al, 1
		
		call printf WRT ..plt

		ADD rsp, 48
		MOV rsp, rbp
		MOV rax, 60
		MOV rdi
		syscall




