#include <windows.h>
extern "C" __declspec(dllexport) 
void FullMap(){
	__asm {
		pushad
		mov ecx, 0x008324E0
		mov ebx, 0x0055A120
		call ebx
		popad
	}
}
extern "C" __declspec(dllexport) 
void ChangeOwnership() {
	__asm {
		pushad
		push 0
		mov eax, 0x00A35DB4
		mov eax, [eax]
		push eax
		mov eax, 0x00A40C64
		mov eax, [eax]
		mov ecx, [eax]
		mov ebx, [ecx]
		call [ebx +0x378]
		popad
	}
}
extern "C" __declspec(dllexport) 
void LevelUp(){
	int number;
	int base;
	__asm{
		push eax
		mov  eax, 0x00A40C70//单位数量
		mov eax, [eax]
		mov number, eax
		mov eax, 0x00A40C64	//单位基址
		mov eax, [eax]
		mov base, eax
		pop eax
	}
	while (number != 0){
		__asm{
			pushad
			mov eax, base
			mov edx, [eax]
			add edx, 0x11C
			mov ebx, 0x40000000
			mov[edx], ebx
			popad
		}
		number = number - 1;
		base = base + 4;
	}
}
extern "C" __declspec(dllexport) 
void CanDeploy() {
	__asm {
		mov eax, 1
		retn 0x10
	}
}
//void RemoteCall(HANDLE process,LPVOID function) {
//	DWORD thread;
//	LPVOID address = VirtualAllocEx(process, NULL, 0x256, MEM_COMMIT, PAGE_EXECUTE_READWRITE);
//	WriteProcessMemory(process, address, function, 0x256, NULL);
//	HANDLE remote = CreateRemoteThread(process, NULL, 0, (LPTHREAD_START_ROUTINE)address, 0, 0, &thread);
//}
